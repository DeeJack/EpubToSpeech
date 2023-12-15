import io
import json

def test_storage(client):
    # Test storing a file
    response = client.post('/internal/audio_storage/store-file', data={'file': (io.BytesIO(b'Hello World'), 'hello_world.txt'), 'filename': 'hello_world.txt'}, content_type='multipart/form-data')
    assert response.status_code == 200
    # assert response.data == b'OK'
    
    # Test getting a file
    response = client.get('/internal/audio_storage/get-file/hello_world.txt')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert data['content'] == "Hello World"
    
    # Test getting a nonexistent file
    response = client.get('/internal/audio_storage/get-file/nonexistent.txt')
    assert response.status_code == 404
    
    # Test getting a file with a path
    response = client.get('/internal/audio_storage/get-file/../../hello_world.txt')
    # assert response.status_code == 400
    
    # Test storing a file with a path
    response = client.post('/internal/audio_storage/store-file', data={'file': (io.BytesIO(b'Hello World'), '../../hello_world.txt')})
    assert response.status_code == 400