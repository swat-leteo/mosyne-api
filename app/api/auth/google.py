"""
Oauth implementation to handle google auth.
"""

# OAuth
from authlib.integrations.starlette_client import OAuth

# Settings
from config import settings

GOOGLE_OAUTH_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_OAUTH_SCOPES = "openid email profile"


oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_OAUTH_URL,
    client_kwargs={"scope": GOOGLE_OAUTH_SCOPES},
)
