# backend/api/payments.py
# Payment processing endpoints

import logging
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import Game, Transaction
from backend.schemas import GamePublish, TransactionResponse, PaymentMethod
from backend.services.payment import PaymentProcessor
from backend.services.dojo_engine import DojoEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["payments"])
payment_processor = PaymentProcessor()


def get_db():
    """Database dependency - will be imported from main.py"""
    pass


@router.get("/methods")
async def get_payment_methods():
    """Get available payment methods"""
    return await payment_processor.get_payment_methods()


@router.post("/publish", response_model=dict)
async def publish_game(publish_request: GamePublish, db: Session = Depends(get_db)):
    """Publish game to mobile platforms with payment"""
    logger.info(f"Publishing game: {publish_request.game_id}")
    
    game = db.query(Game).filter(Game.game_id == publish_request.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Deploy contracts
    contracts = await DojoEngine.deploy_game_contracts(
        publish_request.game_id,
        game.dojo_contract_address
    )
    
    # Process payment
    if publish_request.payment_method == PaymentMethod.CHIPI_PAY:
        tx_hash = await payment_processor.process_starknet_payment(
            from_address=game.developer.wallet_address,
            to_address="0x_platform_address",
            amount=publish_request.payment_amount
        )
    else:
        tx_hash = await payment_processor.process_bitcoin_payment(
            method=publish_request.payment_method.value,
            from_address=game.developer.wallet_address,
            to_address="platform_btc_address",
            amount=float(publish_request.payment_amount)
        )
    
    # Update game status
    game.status = "published"
    game.published_at = datetime.utcnow()
    db.commit()
    
    # Record transaction
    transaction = Transaction(
        transaction_id=f"tx_{uuid.uuid4().hex[:16]}",
        user_id=game.developer_id,
        payment_method=publish_request.payment_method.value,
        amount=publish_request.payment_amount,
        currency="STRK" if publish_request.payment_method == PaymentMethod.CHIPI_PAY else "BTC",
        status="completed",
        blockchain_tx_hash=tx_hash
    )
    db.add(transaction)
    db.commit()
    
    return {
        "message": "Game published successfully",
        "game_id": publish_request.game_id,
        "contracts": contracts,
        "transaction_hash": tx_hash,
        "status": "live",
        "platforms": ["iOS", "Android", "Web"]
    }


@router.get("/history")
async def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    """Get user payment history"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return {"transactions": transactions}


@router.get("/{transaction_id}")
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Get transaction details"""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction
