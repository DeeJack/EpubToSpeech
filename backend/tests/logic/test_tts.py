import os

def test_tts_logic(client):
    response = client.post('/internal/tts/', json={
        'text': 'Test TTS message',
        'service': 'local'
    })
    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=local_tts_output.wav'
    
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", 'local_tts2.wav'), 'wb') as f:
        f.write(response.data)
    
    return
    
    response = client.post('/internal/tts', json={
        'text': 'Hello',
        'service': 'azure'
    })
    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=azure_tts_output.wav'
    
    response = client.post('/internal/tts', json={
        'text': 'Hello',
        'service': 'openai'
    })
    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=openai_tts_output.wav'
    
    response = client.post('/internal/tts', json={
        'text': 'Hello',
        'service': 'elevenlabs'
    })
    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=elevenlabs_tts_output.wav'