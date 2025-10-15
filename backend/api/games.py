# backend/api/games.py
# Game management endpoints

import logging
import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from backend.models import Game, GameAsset
from backend.schemas import GameCreate, GameResponse
from backend.services.dojo_engine import DojoEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])


def get_db():
    """Database dependency - will be imported from main.py"""
    pass


@router.get("/templates")
async def get_templates():
    """Get all available open-source game templates"""
    templates = await DojoEngine.get_game_templates()
    return {"templates": templates}


@router.post("/create", response_model=dict)
async def create_game(game: GameCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new game project"""
    logger.info(f"Creating game: {game.title}")
    
    # Generate unique game ID
    game_id = f"game_{uuid.uuid4().hex[:12]}"
    
    # Create Dojo world
    world_address = await DojoEngine.create_game_world(game.title, game.template_type.value)
    
    new_game = Game(
        game_id=game_id,
        title=game.title,
        description=game.description,
        template_type=game.template_type.value,
        developer_id=user_id,
        dojo_contract_address=world_address
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    
    return {
        "game_id": game_id,
        "title": game.title,
        "world_address": world_address,
        "status": "created",
        "message": "Game project created successfully"
    }


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: str, db: Session = Depends(get_db)):
    """Get game details"""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game


@router.post("/upload")
async def upload_game_assets(
    game_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload game assets"""
    logger.info(f"Uploading assets for game: {game_id}")
    
    # Save file
    upload_dir = Path("uploads") / game_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Save to database
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    asset = GameAsset(
        game_id=game.id,
        asset_type=file.content_type,
        file_path=str(file_path),
        file_size=len(content)
    )
    db.add(asset)
    db.commit()
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": len(content)
    }


@router.get("/{game_id}/stats")
async def get_game_stats(game_id: str, db: Session = Depends(get_db)):
    """Get game statistics and analytics"""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    stats = {
        "game_id": game_id,
        "title": game.title,
        "status": game.status,
        "created_at": game.created_at.isoformat(),
        "published_at": game.published_at.isoformat() if game.published_at else None,
        "total_assets": len(game.assets),
        "contract_address": game.dojo_contract_address,
        "players": 0,
        "revenue": "0 STRK"
    }
    
    return stats


@router.delete("/{game_id}")
async def delete_game(game_id: str, db: Session = Depends(get_db)):
    """Delete a game"""
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(game)
    db.commit()
    
    return {"message": "Game deleted successfully"}
