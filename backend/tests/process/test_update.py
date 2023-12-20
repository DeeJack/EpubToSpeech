import os

def test_update(client):
    # Upload a book
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
        
        id = response.json['id']
    
        # Update the book's info
        response = client.put(
            "/api/update_info/",
            json={
                "book_id": id,
                "title": "Updated Title",
                "author": "Update Author",
                "description": "Updated Description",
            },
        )
        assert response.status_code == 200