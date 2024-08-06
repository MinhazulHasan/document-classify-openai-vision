from unittest.mock import patch, MagicMock
from app.services.image_service import get_image_description

def test_get_image_description(mock_openai_response):
    with patch("app.services.image_service.requests.post") as mock_post:
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = mock_openai_response
        
        result = get_image_description("base64_encoded_image")
    
    assert result == "This is a test response."
    mock_post.assert_called_once()