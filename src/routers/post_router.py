from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.controllers.post_controller import PostController
from src.dependencies.posts import get_post_controller
from src.schemas.posts import PostFullDto, PostWrite

router = APIRouter(prefix="/post", tags=["Посты"])
Controller = Annotated[PostController, Depends(get_post_controller)]
PostId = Annotated[int, Path(ge=1, description="Идентификатор поста", examples=[1])]
NOT_FOUND = {404: {"description": "Пост не найден"}}


@router.get("/many", summary="Список постов")
async def list_posts(controller: Controller) -> list[PostFullDto]:
    return await controller.list()


@router.get("/{post_id}", summary="Получить пост", responses=NOT_FOUND)
async def get_post(post_id: PostId, controller: Controller) -> PostFullDto:
    return await controller.get(post_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Создать пост")
async def create_post(data: PostWrite, controller: Controller) -> PostFullDto:
    return await controller.create(data)


@router.put("/{post_id}", summary="Обновить пост", responses=NOT_FOUND)
async def update_post(post_id: PostId, data: PostWrite, controller: Controller) -> PostFullDto:
    return await controller.update(post_id, data)


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пост",
    responses=NOT_FOUND,
)
async def delete_post(post_id: PostId, controller: Controller) -> Response:
    await controller.delete(post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
