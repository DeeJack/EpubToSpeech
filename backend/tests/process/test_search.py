def test_search(client):
    response = client.get("/api/search/?keywords=title")
    print(response)
    assert response.status_code == 200
    assert response.json != []
    print(response.json)
    
    # Try with a keyword that doesn't exist
    response = client.get("/api/search/?keywords=asdfghjkl")
    assert response.status_code == 404
    
    # Try with a keyword that is too short
    response = client.get("/api/search/?keywords=as")
    assert response.status_code == 400