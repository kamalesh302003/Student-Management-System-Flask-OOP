from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if AuthService.authenticate(username, password):
            user = AuthService.get_user_by_username(username)
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful.', 'success')
            return redirect(url_for('students.index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            success, message = AuthService.register_user(username, email, password)
            if success:
                flash(message, 'success')
                return redirect(url_for('auth.login'))
            flash(message, 'danger')
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user = AuthService.get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user.get_details())

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            success, message = AuthService.change_password(
                session['user_id'], old_password, new_password
            )
            flash(message, 'success' if success else 'danger')
            if success:
                return redirect(url_for('auth.profile'))
    return render_template('change_password.html')
