import os

def test_upload(client):
    with open(os.path.join(os.path.dirname(__file__), '..',  'test_files', 'test.epub'), 'rb') as f:
        response = client.post(
            '/api/upload/',
            data={
                'file': f
            }
        )
        assert response.status_code == 200
        assert response.json['title'] == 'A Study in Scarlet'
        assert response.json['author'] == 'Arthur Conan Doyle'
        assert response.json['id'] != '' and response.json['id'] is not None
    
    
    with open(os.path.join(os.path.dirname(__file__), '..',  'test_files', 'azure_tts.wav'), 'rb') as f:
        response = client.post(
            '/api/upload/',
            data={
                'file': f
            }
        )
        assert response.status_code != 200
    
    with open(os.path.join(os.path.dirname(__file__), '..',  'test_files', 'large_file'), 'rb') as f:
        response = client.post(
            '/api/upload/',
            data={
                'file': f
            }
        )
        assert response.status_code != 200