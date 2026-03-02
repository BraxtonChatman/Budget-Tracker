from app.models import User
from app.extensions import db


def register_account(username, password):

    errors = []
    username = username.strip()
    if User.query.filter_by(username=username).first():
            errors.append("Username already exists")
            return False, errors
        
    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return True, errors

def authenticate_user(username, password):
    errors = []
    username = username.strip()

    if not username:
         errors.append("Username is required.")
    
    if not password:
         errors.append("Password is required")
   
    if errors:
         return None, errors
    
    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        errors.append("Invalid username or password")  
        return None, errors
    
    return user, errors
      