from datetime import UTC, datetime

from jose import JWTError, jwt

from settings import app_settings
from src.enums.auth import TokenKind
from src.exceptions.auth import InvalidToken
from src.schemas.auth import TokenDto

ALGORITHM = "HS256"
ISSUER = "blog-api"


def encode_token(data: TokenDto, kind: TokenKind) -> str:
    return jwt.encode(
        {
            "iss": ISSUER,
            "sub": str(data.user_id),
            "jti": str(data.id),
            "iat": int(data.created_at.timestamp()),
            "exp": int(data.expire_at.timestamp()),
            "type": kind.value,
        },
        app_settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_token(value: str, kind: TokenKind) -> TokenDto:
    try:
        payload = jwt.decode(
            value,
            app_settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            options={
                "require_iss": True, "require_sub": True, "require_jti": True,
                "require_iat": True, "require_exp": True,
            },
        )
        if payload.get("type") != kind.value:
            raise InvalidToken()
        token_id, user_id = int(payload["jti"]), int(payload["sub"])
        if not (0 < token_id <= 2**31 - 1 and 0 < user_id <= 2**31 - 1):
            raise InvalidToken()
        return TokenDto(
            id=token_id,
            user_id=user_id,
            created_at=datetime.fromtimestamp(payload["iat"], UTC),
            expire_at=datetime.fromtimestamp(payload["exp"], UTC),
        )
    except (JWTError, ValueError, OverflowError, OSError, TypeError) as exc:
        raise InvalidToken() from exc
