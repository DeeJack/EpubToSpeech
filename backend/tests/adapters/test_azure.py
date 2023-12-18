import os

def test_azure(client):
    data = {
        'text': 'Hello world!'
    }
    response = client.post('/internal/azure/tts', json=data)
    assert response.status_code == 200
    assert response.content_type == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=azure_tts_output.wav'
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", 'azure_tts.wav'), 'wb') as f:
        f.write(response.data)