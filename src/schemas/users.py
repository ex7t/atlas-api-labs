from typing import Annotated

from pydantic import AfterValidator, EmailStr, Field, SecretStr, StringConstraints

from .common import BaseSchema

Username = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
Login = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
Email = Annotated[EmailStr, Field(max_length=120)]


def validate_password(password: SecretStr) -> SecretStr:
    value = password.get_secret_value()
    if len(value) < 8 or len(value.encode("utf-8")) > 72:
        raise ValueError("Пароль должен содержать минимум 8 символов и не более 72 байт в UTF-8")
    return password


Password = Annotated[SecretStr, AfterValidator(validate_password)]


class UserWrite(BaseSchema):
    username: Username
    email: Email
    login: Login
    password: Password


class UserFullDto(BaseSchema):
    id: int = Field(ge=1)
    username: Username
    email: Email
    login: Login


class PublicUserDto(BaseSchema):
    id: int = Field(ge=1)
    username: Username
