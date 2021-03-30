from api import firebase
from api.models.auth import AddUserRequest, AddUserResponse, DelUserRequest
from api.models.common import APIResponse

import uuid

from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/add_user")
async def add_user(request: AddUserRequest) -> APIResponse:
    user = firebase.get_user(username=request.admin, collection="Admin")

    if isinstance(user.to_dict(), dict):
        if request.token not in user.to_dict()["token"]:
            return APIResponse(status=404, message="USER_NOT_FOUND")
    else:
        return APIResponse(status=404, message="USER_NOT_FOUND")

    data = {"device": request.device, "token": uuid.uuid4().hex}
    firebase.create_user(collection="Users", username=request.name, data=data)

    return AddUserResponse(status=200, message=data)


@router.post("/delete_user")
async def delete_user(request: DelUserRequest) -> APIResponse:
    user = firebase.get_user(username=request.admin, collection="Admin")

    if isinstance(user.to_dict(), dict):
        if request.token not in user.to_dict()["token"]:
            return APIResponse(status=404, message="USER_NOT_FOUND")
    else:
        return APIResponse(status=404, message="USER_NOT_FOUND")

    firebase.delete_user(username=request.name, collection="Users")

    return APIResponse(status=200, message="SUCCESSFULLY_DELETED_USER")
