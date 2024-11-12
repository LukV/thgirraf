from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

cred = credentials.Certificate('secrets/firebaseAccountKey.json')
firebase_admin.initialize_app(cred)

app = FastAPI()

# Allow all origins for testing; in production, specify the allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from the FastAPI backend!"}

security = HTTPBearer()

def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )
    
@app.get('/protected-endpoint')
def protected_endpoint(uid=Depends(verify_firebase_token)):
    # uid is the user's Firebase UID
    return {'message': f'Access granted to user {uid}'}

