from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# In-memory storage for MVP
users_db = {}
patients_db = {}
lab_results_db = {}
audit_logs_db = []

class User:
    def __init__(self, username, email, password, role='clinician'):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role  # 'admin' or 'clinician'
        self.created_at = datetime.utcnow()
        self.is_active = True
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Patient:
    def __init__(self, first_name, last_name, date_of_birth, gender, phone, email, address, medical_record_number=None):
        self.id = str(uuid.uuid4())
        self.medical_record_number = medical_record_number or f"MRN-{self.id[:8]}"
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'id': self.id,
            'medical_record_number': self.medical_record_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class LabResult:
    def __init__(self, patient_id, test_name, test_type, result_value, reference_range, status='completed', notes=''):
        self.id = str(uuid.uuid4())
        self.patient_id = patient_id
        self.test_name = test_name
        self.test_type = test_type
        self.result_value = result_value
        self.reference_range = reference_range
        self.status = status
        self.notes = notes
        self.order_date = datetime.utcnow()
        self.result_date = datetime.utcnow()
        
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'test_name': self.test_name,
            'test_type': self.test_type,
            'result_value': self.result_value,
            'reference_range': self.reference_range,
            'status': self.status,
            'notes': self.notes,
            'order_date': self.order_date.isoformat(),
            'result_date': self.result_date.isoformat()
        }

# Initialize default admin user
admin_user = User('admin', 'admin@healthcare.com', 'admin123', 'admin')
users_db[admin_user.id] = admin_user

# Initialize sample clinician user
clinician_user = User('clinician', 'clinician@healthcare.com', 'clinician123', 'clinician')
users_db[clinician_user.id] = clinician_user
