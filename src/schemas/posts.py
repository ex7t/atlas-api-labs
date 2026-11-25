from datetime import datetime
from typing import Annotated

from pydantic import Field, StringConstraints

from .common import BaseSchema


class PostWrite(BaseSchema):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)] = "Без заголовка"
    author_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class PostFullDto(PostWrite):
    id: int = Field(ge=1, examples=[1])
    created_at: datetime
    is_deleted: bool
    deleted_by: int | None
    deleted_at: datetime | None
