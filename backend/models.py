# backend/models.py
# Database models for Dojo Game Launchpad

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    wallet_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    games = relationship("Game", back_populates="developer")
    transactions = relationship("Transaction", back_populates="user")


class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    template_type = Column(String)
    developer_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="draft")  # draft, published, live
    dojo_contract_address = Column(String, nullable=True)
    game_file_path = Column(String, nullable=True)
    documentation_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    developer = relationship("User", back_populates="games")
    assets = relationship("GameAsset", back_populates="game")


class GameAsset(Base):
    __tablename__ = "game_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    asset_type = Column(String)  # image, audio, code, etc.
    file_path = Column(String)
    file_size = Column(Integer)
    optimized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game = relationship("Game", back_populates="assets")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_method = Column(String)  # chipi_pay, xverse, vesu
    amount = Column(String)
    currency = Column(String)  # STRK, BTC
    status = Column(String)  # pending, completed, failed
    blockchain_tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
