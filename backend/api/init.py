# backend/api/__init__.py
# API modules initialization

from .users import router as users_router
from .games import router as games_router
from .payments import router as payments_router
from .chat import router as chat_router

__all__ = ['users_router', 'games_router', 'payments_router', 'chat_router']
