import io


def test_storage(client):
    # Test storing a file
    response = client.post('/api/audio_storage/store-file', data={'file': (io.BytesIO(b'Hello World'), 'hello_world.txt')})
    assert response.status_code == 200
    assert response.data == b'OK'
    
    # Test getting a file
    response = client.get('/api/audio_storage/get-file/hello_world.txt')
    assert response.status_code == 200
    assert response.data == b'Hello World'
    
    # Test getting a nonexistent file
    response = client.get('/api/audio_storage/get-file/nonexistent.txt')
    assert response.status_code == 404
    
    # Test getting a file with a path
    response = client.get('/api/audio_storage/get-file/../../hello_world.txt')
    assert response.status_code == 400
    
    # Test storing a file with a path
    response = client.post('/api/audio_storage/store-file', data={'file': (io.BytesIO(b'Hello World'), '../../hello_world.txt')})
    assert response.status_code == 400