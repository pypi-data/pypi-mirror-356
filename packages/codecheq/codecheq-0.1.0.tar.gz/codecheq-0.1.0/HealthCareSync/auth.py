from functools import wraps
from flask import session, redirect, url_for, flash, request
from models import users_db
from audit import log_audit_event

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        user = users_db.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Administrative privileges required.', 'error')
            log_audit_event(session['user_id'], 'access_denied', 'admin_area', 
                          details={'attempted_url': request.url})
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        return users_db.get(session['user_id'])
    return None

def authenticate_user(username, password):
    for user in users_db.values():
        if user.username == username and user.check_password(password):
            return user
    return None
