from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image_service import get_image_description
from app.utils.helpers import encode_image

router = APIRouter()

@router.post("/image_description/")
async def image_description(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")
    
    file_content = await file.read()
    base64_image = encode_image(file_content)
    response = get_image_description(base64_image)
    return {"response": response}