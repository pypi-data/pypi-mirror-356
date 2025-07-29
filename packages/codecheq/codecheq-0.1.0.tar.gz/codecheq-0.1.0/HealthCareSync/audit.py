from datetime import datetime
from models import audit_logs_db
import uuid

def log_audit_event(user_id, action, resource_type, resource_id=None, details=None):
    """
    Log audit event for HIPAA compliance
    """
    audit_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,  # create, read, update, delete, login, logout, access_denied
        'resource_type': resource_type,  # patient, lab_result, user, system
        'resource_id': resource_id,
        'details': details or {},
        'ip_address': None,  # Could be enhanced to capture real IP
        'user_agent': None   # Could be enhanced to capture user agent
    }
    
    audit_logs_db.append(audit_entry)
    
    # In production, this would be written to a secure, tamper-proof log system
    print(f"AUDIT: {audit_entry['timestamp']} - User {user_id} performed {action} on {resource_type}")

def get_audit_logs(limit=100, user_id=None, action=None, resource_type=None):
    """
    Retrieve audit logs with optional filtering
    """
    logs = audit_logs_db.copy()
    
    # Apply filters
    if user_id:
        logs = [log for log in logs if log['user_id'] == user_id]
    if action:
        logs = [log for log in logs if log['action'] == action]
    if resource_type:
        logs = [log for log in logs if log['resource_type'] == resource_type]
    
    # Sort by timestamp (most recent first) and limit
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return logs[:limit]

def get_audit_statistics():
    """
    Get audit statistics for reporting
    """
    total_events = len(audit_logs_db)
    
    # Count by action type
    action_counts = {}
    resource_counts = {}
    
    for log in audit_logs_db:
        action = log['action']
        resource = log['resource_type']
        
        action_counts[action] = action_counts.get(action, 0) + 1
        resource_counts[resource] = resource_counts.get(resource, 0) + 1
    
    return {
        'total_events': total_events,
        'action_counts': action_counts,
        'resource_counts': resource_counts
    }
