from enum import Enum, StrEnum


class RegexEnum(str, Enum):
    JWT = r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$"


class TokenKind(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthMessage(StrEnum):
    INVALID_CREDENTIALS = "Неверный логин или пароль"
    INVALID_TOKEN = "Токен недействителен или истёк"
    FORBIDDEN = "Доступ разрешён только к своему профилю"
