from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from firebase_admin import credentials, initialize_app

def initialize_firebase():
    """Initializes Firebase application with credentials."""
    base_path = Path(__file__).resolve().parent.parent  # Get the base directory
    secret_path = base_path / "secrets/firebaseAccountKey.json"
    cred = credentials.Certificate(secret_path)
    initialize_app(cred)

def setup_cors(app: FastAPI):
    """Sets up CORS middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
