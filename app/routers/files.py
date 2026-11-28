import os
import uuid

from fastapi import APIRouter, UploadFile, HTTPException, File,Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import File as FileModel


router = APIRouter(
    prefix="/files",
    tags=["文件管理"]
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
    "image/jpeg": ".jpg"
}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type not in ALLOW_TYPES:
        raise HTTPException(
            status_code=400,
            detail="只允许上传PNG或JPG图片"
        )
    extension = ALLOW_TYPES[file.content_type]

    
    filename = f"{uuid.uuid4()}{extension}"


    file_path = os.path.join(UPLOAD_DIR, filename)

    size = 0
    try:
        with open(file_path,"wb") as f:
            while chunk :=await file.read(1024 * 1024):
                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="文件不能超过5MB"
                    )

                f.write(chunk)

        file_record = FileModel(
            filename=filename,
            original_filename=os.path.basename(file.filename or "unknown"),
            content_type=file.content_type,
            size=size
        )

        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        return{
            "message":"文件上传成功",
            "file_id":file_record.id,
            "filename":file_record.filename,
            "size":file_record.size
        }

    except Exception:
        db.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise


    finally:
        await file.close()



@router.get("/download/{filename}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    file_record = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="文件记录不存在" 
        )
    file_path = os.path.realpath(
        os.path.join(UPLOAD_DIR, file_record.filename)
    )

    if os.path.commonpath([UPLOAD_DIR, file_path]) != os.path.realpath(UPLOAD_DIR):
        raise HTTPException(
            status_code=400,
            detail="非法文件路径"
        )

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail="服务器文件不存在"
        )

    return FileResponse(
        path=file_path,
        filename=file_record.original_filename,
        media_type=file_record.content_type
    )
