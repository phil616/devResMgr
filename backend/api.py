from fastapi import APIRouter
from hashlib import sha256
from setting import settings
from fastapi import Header, HTTPException, Depends
from typing_extensions import Annotated
from pydantic import BaseModel
from model import User

class UserSchema(BaseModel):
    username: str
    password: str

def create_token(user_id: int) -> str:
    """Gen token, token structure = uid.sha256(uid+secret)"""
    token = f"{user_id}." + sha256((str(user_id) + settings.TOKEN_SECRET).encode()).hexdigest()
    return token

async def verify_token(Token: Annotated[str, Header(...)]):
    """Verify token"""
    try:
        uid, token = Token.split('.')
        assert sha256((uid + settings.TOKEN_SECRET).encode()).hexdigest() == token
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    return uid

auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.post('/login')
async def login(user: UserSchema):
    """Login user"""
    user_obj = await User.filter(username=user.username).first()
    if not user_obj or sha256(user.password.encode()).hexdigest()!= user_obj.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return create_token(user_obj.id)

@auth_router.post('/register')
async def register(token:str, user: UserSchema):
    """Register user"""
    if token != settings.TOKEN_SECRET:
        raise HTTPException(status_code=401, detail="Invalid token")
    await User.create(username=user.username, password=sha256(user.password.encode()).hexdigest())
    return {"message": "User registered successfully"}
