from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()


# ---------- Password hashing ----------

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------- JWT create / verify ----------

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    # expire = datetime.now(timezone.utc) + (
    #     timedelta(expires_delta)
    #     or timedelta(minutes=settings.setting.jwt_access_token_expire_minutes)
    # )
    # to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.setting.jwt_secret_key,
        algorithm=settings.setting.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    token = token.replace("Bearer " , "")
    try:
        payload = jwt.decode(
            token,
            settings.setting.jwt_secret_key,
            algorithms=[settings.setting.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None