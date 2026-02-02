def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Stream-M Backend"}

def test_chat(client):
    response = client.post("/api/v1/chat", json={"message": "hello"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_transcribe_skeleton(client):
    # This is a skeleton test
    response = client.post(
        "/api/v1/transcribe",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 200
    assert "text" in response.json()
