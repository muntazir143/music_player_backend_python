from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader

router = APIRouter()
     
cloudinary.config( 
    cloud_name = "do7oo2wpd", 
    api_key = "357311479883325", 
    api_secret = "<your_api_secret>",
    secure=True
)

@router.post("/upload")
def upload_song(song: UploadFile = File(...), thumbnail: UploadFile = File(...), 
                song_name: str = Form(...), artist: str = Form(...), 
                hex_code: str = Form(...), db: Session=Depends(get_db),
                auth_dict=Depends(auth_middleware)):
    pass