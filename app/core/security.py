from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


class AuthSettings(BaseModel):
    authjwt_secret_key: str = "change-me"
    authjwt_algorithm: str = "HS256"

@AuthJWT.load_config
def get_config():
    return AuthSettings()

