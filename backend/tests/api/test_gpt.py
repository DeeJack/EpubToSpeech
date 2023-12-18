def test_generation(client):
    # if True:
    #     return
    response = client.post(
        "internal/openai/text-generation",
        json={"prompt": "Hello.",
            "pre_prompt": "Answer only with one \"Yes\""},
    )
    assert response.status_code == 200
    print(response.json['text'])
    assert response.json["text"].startswith("Yes")

    if True:
        return
    
    response = client.post(
        "internal/openai/image-generation",
        json={"text": "Generate the image of a dog"},
    )
    print(response.json['image'])
    assert response.status_code == 200
    assert response.json["image"] != ""
    
    response = client.post(
        "internal/openai/tts",
        json={"text": "Hello World"},
    )
    assert response.status_code == 200
    assert response.data != b""