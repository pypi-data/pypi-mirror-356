from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    model_config = {
        "arbitrary_types_allowed": True
    }


class UserRequest(BaseModel):
    username: str
    email: str
    userId: str
    jwt: str
    settings: [str]
    model_config = {
        "arbitrary_types_allowed": True
    }


class SettingsRequest(BaseModel):
    type: str
    is_default: bool
    id: int
    name: str
    wt: str
    settings: str
    model_config = {
        "arbitrary_types_allowed": True
    }

