from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.s3 import s3_client
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class ImageResponse(BaseModel):
    url: str
    filename: str

@router.post("/upload/", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: Optional[str] = "images"
):
    """Upload an image to S3 and return its URL"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        url = await s3_client.upload_file(file, folder)
        return {
            "url": url,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
async def delete_image(file_url: str):
    """Delete an image from S3"""
    try:
        await s3_client.delete_file(file_url)
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 