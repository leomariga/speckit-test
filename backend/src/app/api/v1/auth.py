"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...config import settings
from ...db.mongodb import get_db
from ...db.models.user import UserDB
from ...services.auth_service import AuthService
from ...models.user import UserResponse


router = APIRouter()


# OAuth scopes
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


def get_oauth_flow():
    """Create OAuth flow."""
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )


def get_auth_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> AuthService:
    """Dependency for auth service."""
    user_db = UserDB(db)
    return AuthService(user_db)


def get_session_token(session: Optional[str] = Cookie(None)) -> Optional[str]:
    """Extract session token from cookie."""
    return session


async def get_current_user(
    session: Optional[str] = Depends(get_session_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """Get current authenticated user."""
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return await auth_service.get_current_user(session)


@router.get("/auth/google")
async def initiate_google_auth():
    """
    Initiate Gmail OAuth flow.
    Redirects user to Google OAuth consent screen.
    """
    try:
        flow = get_oauth_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # In production, store state in session for CSRF protection
        return RedirectResponse(url=authorization_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate OAuth: {str(e)}"
        )


@router.get("/auth/google/callback")
async def handle_google_callback(
    code: str,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Handle Google OAuth callback.
    Creates/updates user and sets session cookie.
    """
    try:
        # Exchange code for token
        flow = get_oauth_flow()
        flow.fetch_token(code=code)
        
        # Get user info from token
        credentials = flow.credentials
        google_user_info = await auth_service.verify_google_token(credentials.id_token)
        
        # Authenticate or create user
        user = await auth_service.authenticate_or_create_user(google_user_info)
        
        # Create access token
        access_token = auth_service.create_access_token(str(user['_id']))
        
        # Set httpOnly cookie
        response = RedirectResponse(url=settings.FRONTEND_URL)
        response.set_cookie(
            key="session",
            value=access_token,
            httponly=True,
            secure=True,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
):
    """
    Get current authenticated user information.
    """
    return {
        "id": str(current_user['_id']),
        "email": current_user['email'],
        "plan_type": current_user['plan_type'],
        "total_pages_converted": current_user['total_pages_converted'],
        "account_created_at": current_user['account_created_at'],
        "last_login_at": current_user.get('last_login_at'),
    }


@router.post("/auth/logout")
async def logout(response: Response):
    """
    Logout user by clearing session cookie.
    """
    response.delete_cookie(key="session")
    return {"message": "Logged out successfully"}

