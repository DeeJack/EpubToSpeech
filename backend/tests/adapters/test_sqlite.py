def test_crd(client):
    # Create
    response = client.post("/internal/database/add-book", json={"title": "test", "author": "testt", "description": "testtt", "filepath": "test.epub"})
    assert response.status_code == 201
    id = response.json["id"]
    assert response.json['id'] != None and response.json['id'] != ''
    
    print('ID', id)
    
    # Read
    response = client.get("/internal/database/get-book/" + id)
    assert response.status_code == 200
    
    # Read book not found
    response = client.get("/internal/database/get-book/123456789")
    assert response.status_code == 404
    
    # Delete
    response = client.delete("/internal/database/delete-book", json={"id": id})
    assert response.status_code == 200
    
    # Search by title
    response = client.get("/internal/database/search-book?keywords=tes")
    assert response.status_code == 200
    assert response.json != []

    # Search by title not found
    response = client.get("/internal/database/search-book?keywords=notfound")
    assert response.status_code == 404
    assert response.json == []
    
    # Get all books
    response = client.get("/internal/database/get-books")
    assert response.status_code == 200
    assert response.json != []
    
    # Add a chapter
    response = client.post("/internal/database/add-chapter", json={"book_id": id, "number": 23, "filepath": "test.txt"})
    assert response.status_code == 201
    
    # Get chapter
    response = client.get(f"/internal/database/get-chapter/{id}/{23}")
    assert response.status_code == 200
    assert response.json['filepath'] == "test.txt"
    
    # Get all chapters
    response = client.get(f"/internal/database/get-chapters/{id}")
    assert response.status_code == 200
    assert response.json != []
    
    # Get all chapter of a not existing book
    response = client.get(f"/internal/database/get-chapters/123456789")
    assert response.status_code == 404
    assert response.json == []
    
    # Get chapter for a not existing book
    response = client.get(f"/internal/database/get-chapter/123456789/1")
    assert response.status_code == 404
    assert response.json == {}