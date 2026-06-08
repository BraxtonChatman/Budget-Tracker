from flask import Blueprint, request, jsonify #render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_services import register_account, authenticate_user

api_auth_bp = Blueprint('api_auth', __name__, template_folder='../templates', url_prefix='/api/auth')

# --- REGISTER ---
@api_auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    success, errors, user = register_account(username, password)

    if not success:
        return jsonify({'errors': errors}), 400
    return jsonify({
        'message': 'Account created successfully.',
        'user': {'id': user.id, 'username': user.username}
        }), 201
    
# --- LOGIN ---
@api_auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    user, errors = authenticate_user(username, password)

    if user is None:
        return jsonify({'errors': errors}), 401
    
    login_user(user)
    # return jsonify({'user_id': user.id, 'message': 'User logged in successfully.'}), 200
    return jsonify({
        'message': 'User logged in successfully.',
        'user': {'id': user.id, 'username': user.username}
        }), 200
    
# --- LOGOUT ---
@api_auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out successfully.'}), 200

# --- ME ---
@api_auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'is_authenticated': True
    }), 200 
