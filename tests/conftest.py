import pytest
from app import create_app
from app.extensions import db
from app.models import User, Category

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_user(app):
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_form(test_category):
    form = {
        'date': '2026-03-08',
        'category': str(test_category.id),
        'description': 'A test transaction',
        'amount': '108.29',
        'type': 'Income'
    }
    return form

@pytest.fixture
def test_category(app):
    category = Category(id=1, name='Food')
    db.session.add(category)
    db.session.commit()
    return category
