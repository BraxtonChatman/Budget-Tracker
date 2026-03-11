import pytest
from app import create_app
from app.extensions import db
from app.models import User, Category, Transaction, TransactionType
from datetime import date
from decimal import Decimal

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
def another_user(app):
    user = User(username='anotheruser')
    user.set_password('12345678')
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
def invalid_form(test_category):
    form = {
        'date': '1',
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

@pytest.fixture
def test_category2(app):
    category = Category(id=2, name='test')
    db.session.add(category)
    db.session.commit()
    return category

@pytest.fixture
def test_tx_for_test_user(test_user, test_category):
    tx = Transaction(
        date = date(2026, 3, 5),
        category_id = test_category.id,
        user_id = test_user.id,
        description = 'Test transaction for user: testuser',
        amount = Decimal('25.50'),
        type = TransactionType.Expense
    )
    db.session.add(tx)
    db.session.commit()
    return tx

@pytest.fixture
def test_tx_for_test_user2(test_user, test_category2):
    tx = Transaction(
        date = date(2026, 3, 8),
        category_id = test_category2.id,
        user_id = test_user.id,
        description = 'Test transaction for user: testuser',
        amount = Decimal('12.67'),
        type = TransactionType.Income
    )
    db.session.add(tx)
    db.session.commit()
    return tx

@pytest.fixture
def create_tx_for_testuser(test_user, test_category):
    def _create(amount, tx_type):
        tx = Transaction(
            date = date.today(),
            category_id = test_category.id,
            user_id = test_user.id,
            description = 'Test tx description',
            amount = Decimal(amount),
            type = tx_type
        )
        return tx
    return _create

@pytest.fixture
def test_tx_for_sorting(test_user, test_category):
    tx1 = Transaction(
        date=date(2026, 3, 8),
        category_id=test_category.id,
        user_id=test_user.id,
        description='test',
        amount=Decimal('1.00'),
        type=TransactionType.Income
    )

    tx2 = Transaction(
        date=date(2026, 3, 7),
        category_id=test_category.id,
        user_id=test_user.id,
        description='test',
        amount=Decimal('2.00'),
        type=TransactionType.Expense
    )

    tx3 = Transaction(
        date=date(2026, 3, 6),
        category_id=test_category.id,
        user_id=test_user.id,
        description='test',
        amount=Decimal('3.00'),
        type=TransactionType.Income
    )
    db.session.add(tx1)
    db.session.add(tx2)
    db.session.add(tx3)
    db.session.commit()
    
    return [tx1, tx2, tx3]