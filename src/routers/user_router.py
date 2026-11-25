from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.controllers.user_controller import UserController
from src.dependencies.users import get_user_controller
from src.schemas.users import UserFullDto, UserWrite

router = APIRouter(prefix="/user", tags=["Пользователи"])
Controller = Annotated[UserController, Depends(get_user_controller)]
UserId = Annotated[int, Path(ge=1, description="Идентификатор пользователя")]


@router.get("/many", summary="Список пользователей")
async def list_users(controller: Controller) -> list[UserFullDto]:
    return await controller.list()


@router.get("/{user_id}", summary="Получить пользователя")
async def get_user(user_id: UserId, controller: Controller) -> UserFullDto:
    return await controller.get(user_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
async def create_user(data: UserWrite, controller: Controller) -> UserFullDto:
    return await controller.create(data)


@router.put("/{user_id}", summary="Обновить пользователя")
async def update_user(user_id: UserId, data: UserWrite, controller: Controller) -> UserFullDto:
    return await controller.update(user_id, data)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пользователя"
)
async def delete_user(user_id: UserId, controller: Controller) -> Response:
    await controller.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
