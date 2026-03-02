from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_services import register_account, authenticate_user

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

# --- REGISTER ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        success, errors = register_account(username, password)
        if not success:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('auth.register'))

        flash("Account created. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# --- LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user, errors = authenticate_user(username, password)

        if not user:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for('transactions.index'))
            
    return render_template('login.html')


# --- LOGOUT ---
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))