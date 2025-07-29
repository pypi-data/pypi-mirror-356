from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response
from app import app
from models import User, Patient, users_db, patients_db, LabResult, lab_results_db
from auth import login_required, admin_required, authenticate_user, get_current_user
from audit import log_audit_event, get_audit_logs, get_audit_statistics
from lab_integration import HL7MockIntegration, get_lab_results_for_patient, get_all_lab_results
from datetime import datetime
import json
import csv
import io

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            log_audit_event(user.id, 'login', 'system', details={'username': username})
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            log_audit_event(None, 'failed_login', 'system', details={'username': username})
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    user_id = session.get('user_id')
    log_audit_event(user_id, 'logout', 'system')
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    
    # Get dashboard statistics
    total_patients = len(patients_db)
    total_lab_results = len(lab_results_db)
    pending_results = len([r for r in lab_results_db.values() if r.status == 'pending'])
    
    # Get recent activity
    recent_logs = get_audit_logs(limit=10)
    
    log_audit_event(user.id, 'view', 'dashboard')
    
    return render_template('dashboard.html', 
                         user=user,
                         total_patients=total_patients,
                         total_lab_results=total_lab_results,
                         pending_results=pending_results,
                         recent_logs=recent_logs)

@app.route('/patients')
@login_required
def patients():
    user = get_current_user()
    search = request.args.get('search', '')
    
    # Get all patients
    patient_list = []
    for patient in patients_db.values():
        patient_dict = patient.to_dict()
        # Add lab results count
        patient_dict['lab_results_count'] = len([r for r in lab_results_db.values() if r.patient_id == patient.id])
        patient_list.append(patient_dict)
    
    # Filter by search term
    if search:
        patient_list = [p for p in patient_list if 
                       search.lower() in p['first_name'].lower() or 
                       search.lower() in p['last_name'].lower() or 
                       search.lower() in p['medical_record_number'].lower()]
    
    # Sort by last name
    patient_list.sort(key=lambda x: x['last_name'])
    
    log_audit_event(user.id, 'view', 'patients', details={'search': search})
    
    return render_template('patients.html', patients=patient_list, search=search)

@app.route('/patients/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            patient = Patient(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=request.form['date_of_birth'],
                gender=request.form['gender'],
                phone=request.form['phone'],
                email=request.form['email'],
                address=request.form['address']
            )
            
            patients_db[patient.id] = patient
            
            log_audit_event(user.id, 'create', 'patient', patient.id, 
                          {'name': f"{patient.first_name} {patient.last_name}"})
            
            flash(f'Patient {patient.first_name} {patient.last_name} created successfully.', 'success')
            return redirect(url_for('patient_detail', patient_id=patient.id))
            
        except Exception as e:
            flash(f'Error creating patient: {str(e)}', 'error')
    
    return render_template('patients.html', show_form=True)

@app.route('/patients/<patient_id>')
@login_required
def patient_detail(patient_id):
    user = get_current_user()
    patient = patients_db.get(patient_id)
    
    if not patient:
        flash('Patient not found.', 'error')
        return redirect(url_for('patients'))
    
    # Get lab results for this patient
    lab_results = get_lab_results_for_patient(patient_id)
    
    log_audit_event(user.id, 'view', 'patient', patient_id, 
                  {'name': f"{patient.first_name} {patient.last_name}"})
    
    return render_template('patient_detail.html', patient=patient.to_dict(), lab_results=lab_results)

@app.route('/lab-results')
@login_required
def lab_results():
    user = get_current_user()
    
    # Get all lab results with patient information
    results = get_all_lab_results()
    
    log_audit_event(user.id, 'view', 'lab_results')
    
    return render_template('lab_results.html', lab_results=results)

@app.route('/lab-results/order/<patient_id>', methods=['POST'])
@login_required
def order_lab_tests(patient_id):
    user = get_current_user()
    patient = patients_db.get(patient_id)
    
    if not patient:
        flash('Patient not found.', 'error')
        return redirect(url_for('patients'))
    
    try:
        # Mock lab order
        test_orders = [
            {
                'test_name': request.form.get('test_name', 'Complete Blood Count'),
                'test_type': request.form.get('test_type', 'Hematology'),
                'reference_range': request.form.get('reference_range', 'Normal ranges apply')
            }
        ]
        
        success = HL7MockIntegration.send_lab_order(patient_id, test_orders)
        
        if success:
            log_audit_event(user.id, 'create', 'lab_order', patient_id, 
                          {'test_name': test_orders[0]['test_name']})
            flash('Lab order submitted successfully.', 'success')
        else:
            flash('Error submitting lab order.', 'error')
            
    except Exception as e:
        flash(f'Error ordering lab tests: {str(e)}', 'error')
    
    return redirect(url_for('patient_detail', patient_id=patient_id))

@app.route('/audit-logs')
@admin_required
def audit_logs():
    user = get_current_user()
    
    # Get filters from query parameters
    limit = int(request.args.get('limit', 100))
    filter_user_id = request.args.get('user_id')
    filter_action = request.args.get('action')
    filter_resource = request.args.get('resource_type')
    
    # Get filtered logs
    logs = get_audit_logs(limit=limit, user_id=filter_user_id, 
                         action=filter_action, resource_type=filter_resource)
    
    # Add user information to logs
    for log in logs:
        if log['user_id']:
            log_user = users_db.get(log['user_id'])
            log['username'] = log_user.username if log_user else 'Unknown'
        else:
            log['username'] = 'System'
    
    log_audit_event(user.id, 'view', 'audit_logs')
    
    return render_template('audit_logs.html', audit_logs=logs)

@app.route('/reports')
@login_required
def reports():
    user = get_current_user()
    
    # Get audit statistics
    audit_stats = get_audit_statistics()
    
    # Get patient statistics
    total_patients = len(patients_db)
    patients_by_gender = {}
    for patient in patients_db.values():
        gender = patient.gender
        patients_by_gender[gender] = patients_by_gender.get(gender, 0) + 1
    
    # Get lab results statistics
    total_lab_results = len(lab_results_db)
    results_by_status = {}
    results_by_type = {}
    
    for result in lab_results_db.values():
        status = result.status
        test_type = result.test_type
        
        results_by_status[status] = results_by_status.get(status, 0) + 1
        results_by_type[test_type] = results_by_type.get(test_type, 0) + 1
    
    log_audit_event(user.id, 'view', 'reports')
    
    return render_template('reports.html',
                         audit_stats=audit_stats,
                         total_patients=total_patients,
                         patients_by_gender=patients_by_gender,
                         total_lab_results=total_lab_results,
                         results_by_status=results_by_status,
                         results_by_type=results_by_type)

@app.route('/export/patients')
@login_required
def export_patients():
    user = get_current_user()
    
    # Create CSV output
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Medical Record Number', 'First Name', 'Last Name', 'Date of Birth', 
                    'Gender', 'Phone', 'Email', 'Address', 'Created Date'])
    
    # Write patient data
    for patient in patients_db.values():
        writer.writerow([
            patient.medical_record_number,
            patient.first_name,
            patient.last_name,
            patient.date_of_birth,
            patient.gender,
            patient.phone,
            patient.email,
            patient.address,
            patient.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=patients_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response.headers["Content-type"] = "text/csv"
    
    log_audit_event(user.id, 'export', 'patients', details={'format': 'csv'})
    
    return response

@app.route('/export/lab-results')
@login_required
def export_lab_results():
    user = get_current_user()
    
    # Create CSV output
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Patient MRN', 'Patient Name', 'Test Name', 'Test Type', 'Result Value', 
                    'Reference Range', 'Status', 'Order Date', 'Result Date', 'Notes'])
    
    # Write lab results data
    results = get_all_lab_results()
    for result in results:
        writer.writerow([
            result.get('medical_record_number', 'N/A'),
            result.get('patient_name', 'N/A'),
            result['test_name'],
            result['test_type'],
            result['result_value'],
            result['reference_range'],
            result['status'],
            datetime.fromisoformat(result['order_date']).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.fromisoformat(result['result_date']).strftime('%Y-%m-%d %H:%M:%S'),
            result['notes']
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=lab_results_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response.headers["Content-type"] = "text/csv"
    
    log_audit_event(user.id, 'export', 'lab_results', details={'format': 'csv'})
    
    return response
