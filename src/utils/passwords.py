import bcrypt
from fastapi.concurrency import run_in_threadpool
from pydantic import SecretStr


async def hash_password(password: SecretStr) -> str:
    hashed = await run_in_threadpool(
        bcrypt.hashpw, password.get_secret_value().encode("utf-8"), bcrypt.gensalt(rounds=12)
    )
    return hashed.decode("ascii")
