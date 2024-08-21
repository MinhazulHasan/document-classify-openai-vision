from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.image_service import get_image_description
from app.services.report_service import generate_report
from app.services.report_service_mixed_data import generate_report_for_mixed_data, get_report
from app.utils.helpers import encode_image
from app.utils.logger import report_logger
from typing import Dict, Any


router = APIRouter()

@router.post("/image_description/")
async def image_description(category: str, file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")
    
    file_content = await file.read()
    base64_image = encode_image(file_content)
    response = get_image_description(category, base64_image)
    return {"response": response}


@router.post("/generate_report/")
async def generate_report_endpoint(background_tasks: BackgroundTasks):
    report_logger.info("Report generation requested")
    background_tasks.add_task(generate_report)
    return {"message": "Report generation started in the background"}


@router.post("/report_for_mixed_data")
async def report_for_mixed_data(background_tasks: BackgroundTasks):
    report_logger.info("Report generation requested for mixed data")
    background_tasks.add_task(generate_report_for_mixed_data)
    return {"message": "Report generation started in the background"}


@router.get("/get_report_for_mixed_data/")
async def get_report_for_mixed_data() -> Dict[str, Any]:
    try:
        report = get_report()
        return report
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report not found")
