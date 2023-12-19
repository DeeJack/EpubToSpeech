import os
import io

def test_tts_process(client):
    # First upload a book
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", 'test2.epub'), 'rb') as f:
        response = client.post('/api/upload/', data={
            'file': f
        })
        
        assert response.status_code == 200
        id = response.json['id']
        
        response = client.post('/api/tts/', json={
            'book_id': id,
            'chapter': 123,
            'service': 'local'
        })
        assert response.status_code == 400
        
        response = client.post('/api/tts/', json={
            'book_id': id,
            'chapter': 3,
            'service': 'local'
        })
        assert response.status_code == 200
        assert response.mimetype == 'audio/wav'
        assert len(response.data) > 0
        
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_files", 'process_tts.wav'), 'wb') as f:
            f.write(response.data)