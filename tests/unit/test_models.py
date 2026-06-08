from app.models import User
from app.extensions import db

def test_set_and_check_password(app):
    user = User(username='alice')
    user.set_password('password')

    assert user.check_password('password') is True
    assert user.check_password('wrong') is False