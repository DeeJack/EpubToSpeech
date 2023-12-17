import os

def test_local(client):
    data = {
        'text': 'Hello world!'
    }
    response = client.post('/internal/local/tts', json=data)
    assert response.status_code == 200
    assert response.content_type == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=local_tts_output.wav'
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", 'tts_local.wav'), 'wb') as f:
        f.write(response.data)