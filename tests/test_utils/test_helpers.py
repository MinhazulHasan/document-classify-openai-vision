from app.utils.helpers import encode_image

def test_encode_image():
    test_image = b"test image content"
    encoded = encode_image(test_image)
    assert isinstance(encoded, str)
    assert encoded == "dGVzdCBpbWFnZSBjb250ZW50"