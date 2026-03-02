from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..extensions import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

# --- REGISTER ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return redirect(url_for('auth.register'))
        
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# --- LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('transactions.index'))
        else:
            flash("Invalid credentials", "error")

    return render_template('login.html')


# --- LOGOUT ---
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))