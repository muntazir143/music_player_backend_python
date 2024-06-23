from fastapi import HTTPException
import uuid
import bcrypt
from models.user import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import db

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(400, "User with the same email already exists!")
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    user_db = User(id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db