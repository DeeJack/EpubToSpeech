import os
import io

def test_epub(client):
    # response = client.post('/internal/storage/store-file', data={'file': (io.BytesIO(b'Hello World'), 'hello_world.txt'), 'filename': 'hello_world.txt'}, content_type='multipart/form-data')
    # assert response.status_code == 200
    

    with open(os.path.join(os.getcwd(), 'tests', 'test_files', 'test.epub'), 'rb') as f:
        response = client.post("/internal/epub/store-book", data={"file": f, "book_id": "0"})
        assert response.status_code == 200
        assert response.json != []
        
    response = client.get("/internal/epub/chapters/test.epub")
    assert response.status_code == 200
    assert response.json != []
    
    response = client.get("/internal/epub/chapter/test.epub/0")
    assert response.status_code == 200
    assert response.data != b""