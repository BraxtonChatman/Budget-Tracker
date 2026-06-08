

def test_register(client):
    response = client.post('/api/auth/register', json={'username': 'TestUsername', 'password': 'TestPassword'})

    assert response.status_code == 201
    data = response.get_json()

    assert data['message'] == 'Account created successfully.'
    assert data['user']['username'] == 'TestUsername'

def test_register_fail(test_user, client):
    username = test_user.username
    response = client.post('/api/auth/register', json={'username': username, 'password': 'TestPassword'})

    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data

def test_login(test_user, client):
    username = test_user.username
    password = 'password'
    response = client.post('/api/auth/login', json={'username': username, 'password': password})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['user']['username'] == username

def test_login_fail(client):
    response = client.post('/api/auth/login', json={'username': 'username', 'password': ''})

    assert response.status_code == 401
    data = response.get_json()
    assert 'errors' in data

def test_logout(authenticated_client):
    response = authenticated_client.post('/api/auth/logout')
    assert response.status_code == 200

    response = authenticated_client.get('/api/auth/me')
    assert response.status_code == 401

def test_me(authenticated_client, test_user):
    response = authenticated_client.get('/api/auth/me')
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == test_user.username
    assert data['is_authenticated'] == True

def test_me_fail(client):
    response = client.get('/api/auth/me')
    assert response.status_code == 401
    data = response.get_json()
    assert 'errors' in data