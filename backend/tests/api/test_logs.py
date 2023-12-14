
def test_error_log(client):
    response = client.post('/api/log/error', json={
        'message': 'Test error message'
    })
    assert response.status_code == 200
    
def test_external_api_log(client):
    response = client.post('/api/log/external_api', json={
        'message': 'Test external API message'
    })
    assert response.status_code == 200
    
def test_database_log(client):
    response = client.post('/api/log/database', json={
        'query': 'Test database query'
    })
    assert response.status_code == 200
    
def test_external_api_log_bad_ip(client):
    client.environ_base['REMOTE_ADDR'] = '192.1.1.1'  # Set the IP address
    response = client.post('/api/log/external_api', json={
        'message': 'Test external API message'
    })
    assert response.status_code == 403
    
def test_database_log_bad_ip(client):
    client.environ_base['REMOTE_ADDR'] = '192.1.1.1'  # Set the IP address
    response = client.post('/api/log/database', json={
        'message': 'Test external API message'
    })
    assert response.status_code == 403
    
def test_error_log_bad_ip(client):
    client.environ_base['REMOTE_ADDR'] = '192.1.1.1'  # Set the IP address
    response = client.post('/api/log/error', json={
        'message': 'Test external API message'
    })
    assert response.status_code == 403