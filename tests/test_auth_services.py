from app.services.auth_services import register_account, authenticate_user
from app.models import User
from app.extensions import db

def test_register_account_success(app):
    success, errors = register_account('alice', 'password123')

    assert success is True
    assert errors == []

    user = User.query.filter_by(username='alice').first()
    assert user is not None

def test_register_account_duplicate_username(app, test_user):
    success, errors = register_account('testuser', 'password')

    assert success is False
    assert 'Username already exists' in errors

def test_authenticate_user_no_username(app, test_user):
    user, errors = authenticate_user('', 'password')

    assert user is None
    assert 'Username is required.' in errors

def test_authenticate_user_no_password(app, test_user):
    user, errors = authenticate_user('testuser', '')

    assert user is None
    assert 'Password is required' in errors

def test_authenticate_user_success(app, test_user):
    user, errors = authenticate_user('testuser', 'password')

    assert user is not None
    assert errors == []

def test_authenticate_user_wrong_password(app, test_user):
    user, errors = authenticate_user('testuser', 'wrongPassword')

    assert user is None
    assert 'Invalid username or password' in errors

def test_authenticate_user_wrong_username(app, test_user):
    user, errors = authenticate_user('testuser1', 'wrongPassword')

    assert user is None
    assert 'Invalid username or password' in errors