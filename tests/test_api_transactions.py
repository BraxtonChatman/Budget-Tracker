

def test_get_transactions(authenticated_client):
    response = authenticated_client.get("/api/transactions")

    assert response.status_code == 200
    data = response.get_json()

    assert "transactions" in data