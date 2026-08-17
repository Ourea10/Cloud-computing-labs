import base64
import hashlib
import hmac
import json
import os
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.security_store import USERS, User


security_scheme = HTTPBearer(auto_error=False)

SECRET = os.getenv(
    "API_TOKEN_SECRET",
    "development-only-secret",
)


def _sign(payload: str) -> str:
    signature = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return signature


def create_lab_token(
    username: str,
    expires_in: int = 3600,
) -> str:

    if username not in USERS:
        raise ValueError(
            "Unknown user"
        )

    user = USERS[username]

    payload = {
        "sub": user.user_id,
        "username": user.username,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "exp": int(time.time()) + expires_in,
    }

    encoded_payload = base64.urlsafe_b64encode(
        json.dumps(
            payload,
            separators=(",", ":"),
        ).encode()
    ).decode()

    signature = _sign(encoded_payload)

    return (
        f"{encoded_payload}.{signature}"
    )


def verify_lab_token(
    token: str,
) -> User:

    try:
        encoded_payload, signature = token.split(
            ".",
            maxsplit=1,
        )

        expected_signature = _sign(
            encoded_payload
        )

        if not hmac.compare_digest(
            signature,
            expected_signature,
        ):
            raise ValueError(
                "Invalid signature"
            )

        payload = json.loads(
            base64.urlsafe_b64decode(
                encoded_payload
            )
        )

        if payload["exp"] < int(time.time()):
            raise ValueError(
                "Token expired"
            )

        username = payload["username"]

        return USERS[username]

    except (
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from error


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        security_scheme
    ),
) -> User:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return verify_lab_token(
        credentials.credentials
    )
