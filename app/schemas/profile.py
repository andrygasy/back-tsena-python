from typing import Optional
from pydantic import BaseModel, HttpUrl, validator
import re

class UpdateProfile(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[HttpUrl] = None

    @validator("name")
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError("name must not be empty")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        if v is not None:
            pattern = r"^\+?[0-9]{7,15}$"
            if not re.fullmatch(pattern, v):
                raise ValueError("invalid phone number")
        return v
