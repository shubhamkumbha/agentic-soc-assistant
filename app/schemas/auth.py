from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Request body for user registration."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    """Request body for login."""

    username: str

    password: str


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User information returned by the API."""

    id: int
    username: str

    model_config = {
        "from_attributes": True
    }