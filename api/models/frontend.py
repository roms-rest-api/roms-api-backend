from typing import List
from pydantic import BaseModel

class DeviceVersion(BaseModel):
    version_code: str
    stable: bool

class Device(BaseModel):
    name: str
    brand: str
    codename: str
    supported_versions: List[DeviceVersion]

class DevicesResponse(BaseModel):
    status: int
    message: List[Device]
