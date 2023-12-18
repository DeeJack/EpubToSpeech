def test_gpt_logic(client):
    """
        Test the gpt logic
    """
    
    # Translate
    response = client.post(
        "/internal/gpt/translate", json={"text": "Ciao come va?"}
    )
    assert response.status_code == 200
    print('Translate: ', response.json)
    
    # Summarize
    response = client.post(
        "/internal/gpt/summarize", json={"text": "This is a test text"}
    )
    assert response.status_code == 200
    print('Summarize: ', response.json)
    
    # Generate
    response = client.post(
        "/internal/gpt/generate", json={"prompt": "Answer only with \"Yes.\"", "text": "Hello?"}
    )
    assert response.status_code == 200
    print('Generate: ', response.json)
    
    # Image
    response = client.post(
        "/internal/gpt/image", json={"text": "A drawing of a dog"}
    )
    assert response.status_code == 200
    print('Image: ', response.json)