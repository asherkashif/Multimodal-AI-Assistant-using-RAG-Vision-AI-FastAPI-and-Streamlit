from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import User
from app.services.auth import hash_password
from app.services.auth import (
    hash_password,
    verify_password
)
from app.services.jwt_service import (
    create_access_token
)
from pydantic import BaseModel, EmailStr

router = APIRouter()

class SignupRequest(BaseModel):

    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):

    email: EmailStr
    password: str

@router.post("/signup")
async def signup(
    request: SignupRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(
            request.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "User created successfully."
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }