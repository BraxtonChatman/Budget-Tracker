
def test_get_transactions(authenticated_client):
    response = authenticated_client.get('/api/transactions')

    assert response.status_code == 200
    data = response.get_json()

    assert 'transactions' in data

def test_get_transaction(authenticated_client, test_tx_for_test_user):
    tx_id = test_tx_for_test_user.id

    response = authenticated_client.get(f'/api/transactions/{tx_id}')

    assert response.status_code == 200
    data = response.get_json()

    assert 'transaction' in data
    assert 'categories' in data
    assert data['transaction']['id'] == tx_id

def test_get_transaction_not_found(authenticated_client):
    tx_id = 9999

    response = authenticated_client.get(f'/api/transactions/{tx_id}')

    assert response.status_code == 404
    data = response.get_json()

    assert 'error' in data

def test_post_transaction(authenticated_client, test_category):
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

def test_patch_transaction(authenticated_client, test_tx_for_test_user, test_category):
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

def test_patch_transaction_failure():
    pass

def test_delete_transaction():
    pass

def test_delete_transaction_failure():
    pass