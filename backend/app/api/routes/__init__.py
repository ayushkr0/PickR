from fastapi import APIRouter

from app.api.routes import admin, auth, chat, chat_stream, health, products, sessions

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(chat_stream.router, tags=["chat-stream"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(sessions.router, tags=["sessions"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(products.router, tags=["products"])
