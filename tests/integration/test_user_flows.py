from app.models import Transaction, TransactionType
from decimal import Decimal
from datetime import date
import datetime
from app.extensions import db

def test_full_lifecycle(client, test_category):
    username = 'testUser'
    password = 'password'

    # REGISTER
    response = client.post('/api/auth/register', json={
        'username': username,
        'password': password
    })
    assert response.status_code == 201
    user_id = response.get_json()['user']['id']

    # LOGIN
    response = client.post('/api/auth/login', json={
        'username': username, 
        'password': password
    })
    assert response.status_code == 200

    # VERIFY SESSION
    response = client.get('/api/auth/me')
    assert response.status_code == 200
    assert response.get_json()['username'] == username
    assert response.get_json()['is_authenticated'] is True

    # CREATE TRANSACTION
    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "108.29",
        "type": "Income"
    }
    response = client.post("/api/transactions", json = sample_data)
    assert response.status_code == 201
   
    tx_id = response.get_json()['id']
    tx = db.session.get(Transaction, tx_id)
    assert tx.user_id == user_id

    # GET TRANSACTION
    response = client.get(f'/api/transactions/{tx_id}')
    assert response.status_code == 200
    
    tx_json = response.get_json()['transaction']
    assert tx_json['description'] == sample_data['description']

    # PATCH TRANSACTION
    sample_data_edit = {
        "date": "2026-04-09",
        "category": str(test_category.id),
        "description": "Updated transaction",
        "amount": "108.99",
        "type": "Income"
    }
    response = client.patch(f"/api/transactions/{tx_id}",json = sample_data_edit)
    assert response.status_code == 200

    tx = db.session.get(Transaction, tx_id)
    assert tx.date == datetime.date(2026, 4, 9)
    assert tx.amount == Decimal('108.99')

    # DELETE TRANSACTION
    response = client.delete(f"/api/transactions/{tx_id}")
    assert response.status_code == 200

    # VERIFY
    response = client.get(f"/api/transactions/{tx_id}")
    assert response.status_code == 404

    # LOGOUT
    response = client.post('/api/auth/logout')
    assert response.status_code == 200

    response = client.get('/api/auth/me')
    assert response.status_code == 401

def test_access_restriction(client, test_category):
    username1 = 'testUser1'
    password1 = 'password1'

    username2 = 'testUser2'
    password2 = 'password2'

    # REGISTER
    response = client.post('/api/auth/register', json={
        'username': username1,
        'password': password1
    })
    assert response.status_code == 201

    response = client.post('/api/auth/register', json={
        'username': username2,
        'password': password2
    })
    assert response.status_code == 201
    user2_id = response.get_json()['user']['id']

    # LOGIN USER 1
    response = client.post('/api/auth/login', json={
        'username': username1, 
        'password': password1
    })
    assert response.status_code == 200

    # VERIFY SESSION
    response = client.get('/api/auth/me')
    assert response.status_code == 200
    assert response.get_json()['username'] == username1
    assert response.get_json()['is_authenticated'] is True

    # CREATE TRANSACTION
    sample_data = {
        "date": "2026-03-08",
        "category": str(test_category.id),
        "description": "Test transaction",
        "amount": "108.29",
        "type": "Income"
    }
    response = client.post("/api/transactions", json = sample_data)
    assert response.status_code == 201   
    tx_id = response.get_json()['id']

    # LOGOUT
    response = client.post('/api/auth/logout')
    assert response.status_code == 200

    response = client.get('/api/auth/me')
    assert response.status_code == 401

    # LOGIN USER 2
    response = client.post('/api/auth/login', json={
        'username': username2, 
        'password': password2
    })
    assert response.status_code == 200
    user_data = response.get_json()
    assert user_data['user']['id'] == user2_id
    assert user_data['user']['username'] == username2

    # VERIFY SESSION
    response = client.get('/api/auth/me')
    assert response.status_code == 200
    assert response.get_json()['id'] == user2_id
    assert response.get_json()['username'] == username2
    assert response.get_json()['is_authenticated'] is True

    # GET TRANSACTION
    response = client.get(f'/api/transactions/{tx_id}')
    assert response.status_code in (404, 403)
 
    # LOGOUT
    response = client.post('/api/auth/logout')
    assert response.status_code == 200

    response = client.get('/api/auth/me')
    assert response.status_code == 401   
    
def test_unauthenticated_access_blocked(client):
    # No Login

    # ME
    response = client.get('/api/auth/me')
    assert response.status_code == 401

    # transactions list
    response = client.get('/api/transactions')
    assert response.status_code == 401

    # create transaction
    response = client.post('/api/transactions', json={
        "date": "2026-03-08",
        "category": "1",
        "description": "fail",
        "amount": "10.00",
        "type": "Income"
    })
    assert response.status_code == 401