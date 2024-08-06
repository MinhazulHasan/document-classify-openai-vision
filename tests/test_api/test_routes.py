import io
from unittest.mock import patch

def test_image_description_endpoint(test_client, mock_openai_response):
    test_image = io.BytesIO(b"fake image content")
    
    with patch("app.services.image_service.requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_openai_response
        
        response = test_client.post(
            "/image_description/",
            files={"file": ("test.jpg", test_image, "image/jpeg")}
        )
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"] == "This is a test response."