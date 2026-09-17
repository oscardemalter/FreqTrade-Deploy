from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.config import settings
import time
from collections import defaultdict
from functools import wraps
from flask import request, redirect
from fastapi import Request, HTTPException, status

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
login_attempts = defaultdict(list)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < 300]
    return len(login_attempts[ip]) < 10

def record_attempt(ip: str):
    login_attempts[ip].append(time.time())

def require_auth(f):
    """Décorateur pour protéger les routes Flask"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, redirect, url_for
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for('login'))
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("sub") != settings.ADMIN_EMAIL:
                return redirect(url_for('login'))
        except JWTError:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non authentifié")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("sub") != settings.ADMIN_EMAIL:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non autorisé")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
