from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from app.core.config import settings

class AuthSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = settings.ALGORITHM

@AuthJWT.load_config
def get_config():
    return AuthSettings()

