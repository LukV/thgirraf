import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core.thlogging import configure_logging
from .core.config import setup_cors
from .routers import users, auth
from .db import Base, engine

# Configure logging
configure_logging()

# Create FastAPI app instance
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize configurations
setup_cors(app)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Mount the static images directory at "/icons"
static_icons_dir = os.path.join(os.path.dirname(__file__), "static", "icons")
app.mount("/icons", StaticFiles(directory=static_icons_dir), name="icons")
