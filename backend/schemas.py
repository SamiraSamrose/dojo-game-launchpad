# backend/schemas.py
# Pydantic schemas for request/response validation

from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TemplateType(str, Enum):
    RPG = "rpg"
    PLATFORMER = "platformer"
    CARD_BATTLE = "card"
    STRATEGY = "strategy"
    PUZZLE = "puzzle"
    MULTIPLAYER = "multiplayer"


class PaymentMethod(str, Enum):
    CHIPI_PAY = "chipi_pay"
    XVERSE = "xverse"
    VESU = "vesu"


class UserCreate(BaseModel):
    username: str
    email: str
    wallet_address: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    wallet_address: Optional[str]
    
    class Config:
        from_attributes = True


class GameCreate(BaseModel):
    title: str
    description: str
    template_type: TemplateType


class GameResponse(BaseModel):
    id: int
    game_id: str
    title: str
    description: str
    template_type: str
    status: str
    dojo_contract_address: Optional[str]
    
    class Config:
        from_attributes = True


class GamePublish(BaseModel):
    game_id: str
    payment_method: PaymentMethod
    payment_amount: str


class ChatRequest(BaseModel):
    message: str
    encrypted: bool = True


class ChatResponse(BaseModel):
    message: str
    response: str
    encrypted: bool
    encryption_provider: str


class AIRequest(BaseModel):
    action: str  # publish, docs, optimize
    game_id: str


class TransactionResponse(BaseModel):
    transaction_id: str
    payment_method: str
    amount: str
    currency: str
    status: str
    blockchain_tx_hash: Optional[str]
    
    class Config:
        from_attributes = True
