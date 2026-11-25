import bcrypt
from fastapi.concurrency import run_in_threadpool
from pydantic import SecretStr

DUMMY_HASH = bcrypt.hashpw(b"unused", bcrypt.gensalt(rounds=12)).decode("ascii")


async def hash_password(password: SecretStr) -> str:
    hashed = await run_in_threadpool(
        bcrypt.hashpw, password.get_secret_value().encode("utf-8"), bcrypt.gensalt(rounds=12)
    )
    return hashed.decode("ascii")


async def verify_password(password: SecretStr, hashed: str) -> bool:
    candidate = password.get_secret_value().encode("utf-8")
    if len(candidate) > 72:
        return False
    return await run_in_threadpool(bcrypt.checkpw, candidate, hashed.encode("ascii"))
