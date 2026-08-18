from pydantic import BaseModel


class LoginRequest(BaseModel):

    username: str
    password: str


class LoginResponse(BaseModel):

    access_token: str
    token_type: str = "Bearer"


class CredentialRequest(BaseModel):

    credential_type: str
    value: str


class CredentialResponse(BaseModel):

    credential_id: str
    credential_type: str