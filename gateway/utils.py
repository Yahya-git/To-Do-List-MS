from datetime import datetime, timedelta

from config import settings
from dtos.dto_misc import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_sso.sso.google import GoogleSSO
from jose import JWTError, jwt
from src.exceptions import CreateError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2 = Depends(oauth2_scheme)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_time

google_sso = GoogleSSO(
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    redirect_uri=settings.redirect_url,
    allow_insecure_http=True,
    scope=["openid", "email", "profile"],
)


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        print(f"Exception: {e}")
        raise CreateError from e


def verify_access_token(token: str, credentials_exception):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = decoded_jwt.get("user_id")
        email: str = decoded_jwt.get("user_email")
        expiry = datetime.fromtimestamp(decoded_jwt.get("exp"))
        if expiry < datetime.utcnow():
            raise credentials_exception
        if email is None:
            raise credentials_exception
        if id is None:
            raise credentials_exception
        token_data = TokenData(email=email, id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def validate_user(token: str = oauth2):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'{"could not validate credentials"}',
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_access_token(token, credentials_exception)
    return user
