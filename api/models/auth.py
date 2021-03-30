from pydantic import BaseModel


class AddUserRequest(BaseModel):
    name: str
    device: str
    token: str
    admin: str

class UserAddResponse(BaseModel):
    device: str
    token: str

class AddUserResponse(BaseModel):
    status: int
    message: UserAddResponse

class DelUserRequest(BaseModel):
    token: str
    name: str
    admin: str
