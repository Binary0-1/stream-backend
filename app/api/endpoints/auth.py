from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.token import Token, TokenPayload
from app.schemas.user import User as UserSchema, UserCreate


router = APIRouter()

@router.post("/auth/access-token", response_model=Token)
def access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token_str = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )

    db_refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.utcnow() + refresh_token_expires
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
    }

@router.post("/auth/refresh-token", response_model=Token)
def refresh_token(
    db: Session = Depends(deps.get_db),
    refresh_token: str = Body(...),
) -> Any:
    """
    Refresh tokens using a refresh token
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    db_refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked == False
    ).first()
    
    if not db_refresh_token or db_refresh_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired refresh token")
    
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    db_refresh_token.is_revoked = True
    db.add(db_refresh_token)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    new_access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    new_refresh_token_str = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )

    # Store new refresh token
    new_db_refresh_token = RefreshToken(
        token=new_refresh_token_str,
        user_id=user.id,
        expires_at=datetime.utcnow() + refresh_token_expires
    )
    db.add(new_db_refresh_token)
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "bearer",
    }


@router.post("/auth/register", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    print(user_in.password)
    db_obj = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj