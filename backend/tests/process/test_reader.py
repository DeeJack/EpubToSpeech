import os


def upload_book(client):
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "test_files", "test2.epub"
        ),
        "rb",
    ) as f:
        response = client.post("/api/upload/", data={"file": f})
        assert response.status_code == 200
        id = response.json["id"]
        return id


def test_reader(client):
    id = upload_book(client)
    
    response = client.get(f"/api/reader/chapter/{id}/1")
    assert response.status_code == 200
    print(response.json)
    assert response.json["text"] != ""

    response = client.get(f"/api/reader/chapter/{id}/2000")
    assert response.status_code != 200

    response = client.get(f"/api/reader/chapter/100000/1")
    assert response.status_code != 200

    response = client.get(f"/api/reader/chapter/asd/1")
    assert response.status_code != 200

    response = client.get(f"/api/reader/chapter/1/asd")
    assert response.status_code != 200

    response = client.get(f"/api/reader/chapters/{id}")
    assert response.status_code == 200
    assert len(response.json) > 0

    response = client.get(f"/api/reader/chapters/100000")
    assert response.status_code != 200

def test_translate(client):
    id = upload_book(client)
    
    response = client.post(f"/api/reader/translate/{id}/1")
    assert response.status_code == 200
    assert response.json["text"] != ""
    print(response.json["text"])

    response = client.post(f"/api/reader/translate/{id}/2000")
    assert response.status_code != 200

    response = client.post(f"/api/reader/translate/100000/1")
    assert response.status_code != 200

    response = client.post(f"/api/reader/translate/asd/1")
    assert response.status_code != 200

    response = client.post(f"/api/reader/translate/1/asd")
    assert response.status_code != 200

def test_summarize(client):
    id = upload_book(client)
    
    response = client.post(f"/api/reader/summarize/{id}/1")
    assert response.status_code == 200
    assert response.json["text"] != ""
    print(response.json["text"])

    response = client.post(f"/api/reader/summarize/{id}/2000")
    assert response.status_code != 200

    response = client.post(f"/api/reader/summarize/100000/1")
    assert response.status_code != 200

    response = client.post(f"/api/reader/summarize/asd/1")
    assert response.status_code != 200

    response = client.post(f"/api/reader/summarize/1/asd")
    assert response.status_code != 200
    
def test_image(client):
    response = client.post(f"/api/reader/image/", json={
        'prompt': 'This is a test prompt'
    })
    assert response.status_code == 200
    assert response.json["image"] != ""
    print(response.json["image"])

    response = client.post(f"/api/reader/image/", json={
        'prompt': 'This is a test prompt'*1000
    })
    assert response.status_code != 200

    response = client.post(f"/api/reader/image/", json={
        'prompt': ''
    })
    assert response.status_code != 200