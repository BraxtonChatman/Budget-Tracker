
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
