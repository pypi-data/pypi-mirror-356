from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class UserRequest(BaseModel):
    username: str
    email: str
    userId: str
    jwt: str
    settings: [str]


class SettingsRequest(BaseModel):
    type: str
    is_default: bool
    id: int
    name: str
    wt: str
    settings: str

