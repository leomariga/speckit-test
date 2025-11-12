"""Authentication service with Gmail OAuth."""
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status

from ..config import settings
from ..db.models.user import UserDB
from ..models.user import UserCreate


class AuthService:
    """Authentication service handling OAuth and session management."""
    
    def __init__(self, user_db: UserDB):
        self.user_db = user_db
    
    async def verify_google_token(self, token: str) -> dict:
        """Verify Google OAuth token and extract user info."""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            # Verify token issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            return {
                'email': idinfo['email'],
                'oauth_user_id': idinfo['sub'],
                'name': idinfo.get('name', ''),
            }
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
    
    async def authenticate_or_create_user(self, google_user_info: dict) -> dict:
        """Authenticate existing user or create new user."""
        # Check if user exists by OAuth ID
        user = await self.user_db.get_user_by_oauth_id(
            google_user_info['oauth_user_id']
        )
        
        if user:
            # Update last login
            await self.user_db.update_last_login(str(user['_id']))
            return user
        
        # Check if user exists by email (in case they registered differently)
        user = await self.user_db.get_user_by_email(google_user_info['email'])
        
        if user:
            # Update last login
            await self.user_db.update_last_login(str(user['_id']))
            return user
        
        # Create new user
        user = await self.user_db.create_user(
            email=google_user_info['email'],
            oauth_provider='google',
            oauth_user_id=google_user_info['oauth_user_id'],
            plan_type='free'
        )
        
        return user
    
    def create_access_token(self, user_id: str) -> str:
        """Create JWT access token."""
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return user ID."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None
    
    async def get_current_user(self, token: str) -> dict:
        """Get current user from token."""
        user_id = self.verify_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        user = await self.user_db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user

