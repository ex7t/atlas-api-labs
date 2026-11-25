from itertools import count

from src.schemas.posts import PostFullDto, PostWrite


class PostRepository:
    def __init__(self) -> None:
        self._posts = {
            1: PostFullDto(id=1, author_name="Bob", content="52"),
            2: PostFullDto(id=2, author_name="Billy", content="67"),
            3: PostFullDto(id=3, author_name="John", content="Lorem ipsum"),
        }
        self._ids = count(4)

    async def list(self) -> list[PostFullDto]:
        return list(self._posts.values())

    async def get(self, post_id: int) -> PostFullDto | None:
        return self._posts.get(post_id)

    async def create(self, data: PostWrite) -> PostFullDto:
        post = PostFullDto(id=next(self._ids), **data.model_dump())
        self._posts[post.id] = post
        return post

    async def update(self, post_id: int, data: PostWrite) -> PostFullDto | None:
        if post_id not in self._posts:
            return None
        post = PostFullDto(id=post_id, **data.model_dump())
        self._posts[post_id] = post
        return post

    async def delete(self, post_id: int) -> bool:
        return self._posts.pop(post_id, None) is not None
