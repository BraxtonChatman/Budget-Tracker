from app.models import Transaction, TransactionType
from decimal import Decimal
import datetime
from app.extensions import db

def test_get_transactions(authenticated_client):
    response = authenticated_client.get('/api/transactions')

    assert response.status_code == 200
    data = response.get_json()

    assert 'transactions' in data
    assert "totals" in data
    assert "categories" in data
    assert "errors" in data

def test_get_transaction(authenticated_client, test_tx_for_test_user):
    tx_id = test_tx_for_test_user.id

    response = authenticated_client.get(f'/api/transactions/{tx_id}')

    assert response.status_code == 200
    data = response.get_json()

    tx = data['transaction']

    expected_date = test_tx_for_test_user.date.isoformat() if test_tx_for_test_user.date else None
    expected_type = test_tx_for_test_user.type.value if test_tx_for_test_user.type else None

    assert tx['id'] == tx_id
    assert tx['date'] == expected_date
    assert tx['category_id'] == test_tx_for_test_user.category_id
    assert tx['user_id'] == test_tx_for_test_user.user_id
    assert tx['description'] == test_tx_for_test_user.description
    assert tx['amount'] == float(test_tx_for_test_user.amount)
    assert tx['type'] == expected_type

def test_get_transaction_not_found(authenticated_client):
    tx_id = 9999

    response = authenticated_client.get(f'/api/transactions/{tx_id}')

    assert response.status_code == 404
    data = response.get_json()
    assert 'errors' in data

def test_post_transaction(authenticated_client, test_category, test_user):
    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "108.29",
        "type": "Income"
    }

    response = authenticated_client.post(
        "/api/transactions",
        json = sample_data
    )

    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data

    tx_id = data['id']
    tx = db.session.get(Transaction, tx_id)

    assert tx is not None
    assert tx.date == datetime.date(2026, 3, 8)
    assert tx.category_id == test_category.id
    assert tx.user_id == test_user.id
    assert tx.description == "Test transaction"
    assert tx.amount == Decimal('108.29')
    assert tx.type == TransactionType.Income

def test_post_transaction_failure(authenticated_client, test_category):
    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "-108.29",
        "type": "Income"
    }

    response = authenticated_client.post(
        "/api/transactions",
        json = sample_data
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['errors'] == ["Amount must be greater than zero."]

def test_patch_transaction(authenticated_client, test_tx_for_test_user, test_category, test_user):
    tx_id = test_tx_for_test_user.id
    
    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "108.29",
        "type": "Income"
    }

    response = authenticated_client.patch(
        f"/api/transactions/{tx_id}",
        json = sample_data
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

    tx = db.session.get(Transaction, tx_id)

    assert tx is not None
    assert tx.date == datetime.date(2026, 3, 8)
    assert tx.category_id == test_category.id
    assert tx.user_id == test_user.id
    assert tx.description == "Test transaction"
    assert tx.amount == Decimal('108.29')
    assert tx.type == TransactionType.Income

def test_patch_transaction_failure(authenticated_client, test_category):
    tx_id = 9999

    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "108.29",
        "type": "Income"
    }

    response = authenticated_client.patch(
        f"/api/transactions/{tx_id}",
        json = sample_data
    )

    assert (response.status_code == 400) or (response.status_code == 404)
    data = response.get_json()
    assert 'errors' in data

def test_delete_transaction(authenticated_client, test_tx_for_test_user):
    tx_id = test_tx_for_test_user.id
    
    response = authenticated_client.delete(
        f"/api/transactions/{tx_id}"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    check = authenticated_client.get(f"/api/transactions/{tx_id}")
    assert check.status_code == 404

def test_delete_transaction_failure(authenticated_client):
    tx_id = 9999

    response = authenticated_client.delete(
        f"/api/transactions/{tx_id}"
    )

    assert response.status_code == 404
    data = response.get_json()
    assert 'errors' in data