#!/usr/bin/env python3
"""
AI Meeting Notes Agent - ClickUp Style Platform
Real-time transcription and AI-powered meeting management platform.
"""

import logging
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

# Import our modules
from app.database import engine, get_db
from app import models, auth
from app.routers import auth as auth_router, api, websocket

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Meeting Notes Agent - ClickUp Style",
    version="2.0.0",
    description="AI-powered meeting management platform with real-time collaboration"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_router.router)
app.include_router(api.router)
app.include_router(websocket.router)

@app.get("/")
async def home(
    request: Request,
    current_user: Optional[models.User] = Depends(auth.get_current_active_user_optional)
):
    """Serve the main web interface"""
    if current_user:
        # User is logged in, redirect to dashboard
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        # User not logged in, show login page
        return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Serve the dashboard interface"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/meeting/{meeting_id}")
async def meeting_page(
    request: Request,
    meeting_id: int,
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Serve the meeting interface"""
    return templates.TemplateResponse("meeting.html", {
        "request": request,
        "meeting_id": meeting_id
    })

@app.get("/login")
async def login_page(request: Request):
    """Serve the login interface"""
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )