
def test_error_log(client):
    response = client.post('/api/log/error', data={
        'message': 'Test error message'
    })
    assert response.status_code == 200