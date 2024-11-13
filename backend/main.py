from fastapi import FastAPI
from .core.config import setup_cors
from .routers import users, auth
from .db import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize configurations
setup_cors(app)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
