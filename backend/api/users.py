# backend/api/users.py
# User management endpoints

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import User
from backend.schemas import UserCreate, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    """Database dependency - will be imported from main.py"""
    pass


@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new developer"""
    logger.info(f"Registering user: {user.username}")
    
    # Check if user exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        username=user.username,
        email=user.email,
        wallet_address=user.wallet_address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "message": "User registered successfully"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: int, db: Session = Depends(get_db)):
    """Get current user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/me", response_model=dict)
async def update_user(
    user_id: int,
    username: str = None,
    wallet_address: str = None,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username:
        user.username = username
    if wallet_address:
        user.wallet_address = wallet_address
    
    db.commit()
    
    return {"message": "User updated successfully"}
