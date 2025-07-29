import json
import uuid
from datetime import datetime
from models import LabResult, lab_results_db, patients_db
from audit import log_audit_event

class HL7MockIntegration:
    """
    Mock HL7 integration for lab results
    In production, this would interface with real HL7 systems
    """
    
    @staticmethod
    def process_hl7_message(hl7_message):
        """
        Process incoming HL7 message and create lab result
        """
        try:
            # Mock HL7 parsing - in production would use proper HL7 library
            result = HL7MockIntegration.parse_mock_hl7(hl7_message)
            
            # Create lab result
            lab_result = LabResult(
                patient_id=result['patient_id'],
                test_name=result['test_name'],
                test_type=result['test_type'],
                result_value=result['result_value'],
                reference_range=result['reference_range'],
                status=result.get('status', 'completed'),
                notes=result.get('notes', '')
            )
            
            lab_results_db[lab_result.id] = lab_result
            
            # Log audit event
            log_audit_event('system', 'create', 'lab_result', lab_result.id, 
                          {'source': 'hl7_integration', 'test_name': result['test_name']})
            
            return lab_result
            
        except Exception as e:
            print(f"Error processing HL7 message: {e}")
            return None
    
    @staticmethod
    def parse_mock_hl7(hl7_message):
        """
        Mock HL7 message parser
        """
        # In production, this would properly parse HL7 segments
        return {
            'patient_id': hl7_message.get('patient_id'),
            'test_name': hl7_message.get('test_name'),
            'test_type': hl7_message.get('test_type'),
            'result_value': hl7_message.get('result_value'),
            'reference_range': hl7_message.get('reference_range'),
            'status': hl7_message.get('status', 'completed'),
            'notes': hl7_message.get('notes', '')
        }
    
    @staticmethod
    def send_lab_order(patient_id, test_orders):
        """
        Send lab order to external lab system
        """
        try:
            # Mock lab order processing
            for order in test_orders:
                # Simulate lab processing time by creating pending results
                lab_result = LabResult(
                    patient_id=patient_id,
                    test_name=order['test_name'],
                    test_type=order['test_type'],
                    result_value='Pending',
                    reference_range=order.get('reference_range', 'N/A'),
                    status='pending',
                    notes='Lab order submitted'
                )
                
                lab_results_db[lab_result.id] = lab_result
                
                # Log audit event
                log_audit_event('system', 'create', 'lab_result', lab_result.id, 
                              {'source': 'lab_order', 'test_name': order['test_name']})
            
            return True
            
        except Exception as e:
            print(f"Error sending lab order: {e}")
            return False

def get_lab_results_for_patient(patient_id):
    """
    Get all lab results for a specific patient
    """
    results = []
    for lab_result in lab_results_db.values():
        if lab_result.patient_id == patient_id:
            results.append(lab_result.to_dict())
    
    # Sort by result date (most recent first)
    results.sort(key=lambda x: x['result_date'], reverse=True)
    return results

def get_all_lab_results():
    """
    Get all lab results for reporting
    """
    results = []
    for lab_result in lab_results_db.values():
        result_dict = lab_result.to_dict()
        
        # Add patient information
        patient = patients_db.get(lab_result.patient_id)
        if patient:
            result_dict['patient_name'] = patient.first_name + ' ' + patient.last_name
            result_dict['medical_record_number'] = patient.medical_record_number
        
        results.append(result_dict)
    
    # Sort by result date (most recent first)
    results.sort(key=lambda x: x['result_date'], reverse=True)
    return results
