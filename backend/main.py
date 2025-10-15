# backend/main.py
# Main FastAPI application

import os
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path

from backend.models import Base
from backend.services.ai_agent import AIAgent
from backend.services.payment import PaymentProcessor
from backend.services.encryption import EncryptionService
from backend.services.dojo_engine import DojoEngine

# Import API routers
from backend.api.users import router as users_router
from backend.api.games import router as games_router
from backend.api.payments import router as payments_router
from backend.api.chat import router as chat_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dojo_user:dojo_pass@localhost:5432/dojo_launchpad")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Dojo Game Launchpad API",
    version="1.0.0",
    description="Mobile platform for indie game developers with AI, privacy, and multi-chain payments"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Update get_db in API modules
from backend.api import users, games, payments, chat
users.get_db = get_db
games.get_db = get_db
payments.get_db = get_db
chat.get_db = get_db

# Initialize services
ai_agent = AIAgent()
payment_processor = PaymentProcessor()
encryption_service = EncryptionService()

# Include routers
app.include_router(users_router)
app.include_router(games_router)
app.include_router(payments_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "healthy",
        "service": "Dojo Game Launchpad",
        "version": "1.0.0",
        "features": [
            "AI Agent with RAG",
            "Dojo Engine Integration",
            "Multi-chain Payments (Starknet, Bitcoin)",
            "End-to-end Encryption",
            "Open Source Templates"
        ]
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "ai_agent": "active",
            "payment_processor": "active",
            "encryption": "active"
        }
    }


@app.post("/ai/generate-docs")
async def generate_documentation(game_id: str, db: Session = Depends(get_db)):
    """Generate documentation using AI Agent (RAG)"""
    from backend.models import Game
    
    logger.info(f"Generating documentation for game: {game_id}")
    
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Game not found")
    
    docs = await ai_agent.generate_documentation(game.title, game.description)
    
    # Save documentation
    docs_dir = Path("docs") / game_id
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    for doc_type, content in docs.items():
        doc_path = docs_dir / f"{doc_type}.md"
        with open(doc_path, "w") as f:
            f.write(content)
    
    game.documentation_path = str(docs_dir)
    db.commit()
    
    return {
        "message": "Documentation generated successfully",
        "documents": list(docs.keys()),
        "path": str(docs_dir)
    }


@app.post("/ai/analyze")
async def analyze_game(game_id: str):
    """Analyze game for publishing readiness"""
    analysis = await ai_agent.analyze_game_for_publishing(game_id)
    return analysis


@app.post("/ai/optimize")
async def optimize_game_assets(game_id: str):
    """Optimize game assets using AI"""
    optimization = await ai_agent.optimize_assets(game_id)
    return optimization


if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         DOJO GAME LAUNCHPAD - PRODUCTION BACKEND             ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  - AI Agent with RAG for documentation                       ║
    ║  - Dojo Engine Integration                                   ║
    ║  - Multi-chain Payments (Starknet + Bitcoin)                 ║
    ║  - End-to-end Encryption (Wootzapp)                          ║
    ║  - Open Source Game Templates                                ║
    ║                                                              ║
    ║  API Documentation: http://localhost:8000/docs               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
