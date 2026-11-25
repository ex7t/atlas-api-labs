from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.controllers.user_controller import UserController
from src.dependencies.auth import CurrentUserId, get_current_user_id
from src.dependencies.users import get_user_controller
from src.exceptions.auth import ForbiddenProfile
from src.schemas.users import PublicUserDto, UserFullDto, UserWrite

router = APIRouter(prefix="/user", tags=["Пользователи"])
Controller = Annotated[UserController, Depends(get_user_controller)]
UserId = Annotated[int, Path(ge=1, description="Идентификатор пользователя")]


@router.get("/many", summary="Список пользователей", dependencies=[Depends(get_current_user_id)])
async def list_users(controller: Controller) -> list[PublicUserDto]:
    return [PublicUserDto.model_validate(user) for user in await controller.list()]


@router.get("/{user_id}", summary="Получить пользователя")
async def get_user(user_id: UserId, current_user: CurrentUserId, controller: Controller) -> UserFullDto:
    if user_id != current_user:
        raise ForbiddenProfile()
    return await controller.get(user_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
async def create_user(data: UserWrite, controller: Controller) -> UserFullDto:
    return await controller.create(data)


@router.put("/{user_id}", summary="Обновить пользователя")
async def update_user(
    user_id: UserId, data: UserWrite, current_user: CurrentUserId, controller: Controller
) -> UserFullDto:
    if user_id != current_user:
        raise ForbiddenProfile()
    return await controller.update(user_id, data)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пользователя"
)
async def delete_user(user_id: UserId, current_user: CurrentUserId, controller: Controller) -> Response:
    if user_id != current_user:
        raise ForbiddenProfile()
    await controller.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
