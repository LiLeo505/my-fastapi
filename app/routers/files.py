import os
import uuid

from fastapi import APIRouter, UploadFile, HTTPException, File



router = APIRouter(
    prefix="files",
    tags=["文件上传"]
)

#获取项目根目录
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 5*1024*1024

ALLOW_TYPES = {
    "image/png": ".png",
    "iamge/jpeg": ".jpg"
}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    if file.content_type not in ALLOW_TYPES:
        raise HTTPException(
            status_code=400,
            detail="只允许上传PNG或JPG图片"
        )
    
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="文件不能超过5MB"
        )
    extension = ALLOW_TYPES[file.content_type]

    
    filename = f"{uuid.uuid4()}{extension}"


    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(content)

  

    return {
        "message": "文件上传成功",
        "filename": file.filename
    }