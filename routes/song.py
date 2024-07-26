import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

from models.song import Song

load_dotenv()

router = APIRouter()

api_secret = os.environ.get("CLOUDINARY_API_SECRET")
     
cloudinary.config( 
    cloud_name = "do7oo2wpd", 
    api_key = "357311479883325", 
    api_secret = api_secret,
    secure=True
)

@router.post("/upload", status_code=201)
def upload_song(song: UploadFile = File(...), thumbnail: UploadFile = File(...), 
                song_name: str = Form(...), artist: str = Form(...), 
                hex_code: str = Form(...), db: Session=Depends(get_db),
                auth_dict=Depends(auth_middleware)):
    song_id = str(uuid.uuid4())
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type="image", folder=f"songs/{song_id}")
    song_res = cloudinary.uploader.upload(song.file, resource_type="auto", folder=f"songs/{song_id}")
    
    new_song = Song(
        id = song_id,
        song_name = song_name,
        artist = artist,
        hex_code = hex_code,
        song_url = song_res["url"],
        thumbnail_url = thumbnail_res["url"]
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song