from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routers.authentication_router import router as authentication_router
from src.routers.authorization_router import router as authorization_router
from src.routers.post_router import router as post_router
from src.routers.user_router import router as user_router

from web.docs import install_docs

app = FastAPI(title="Мой блог", version="1.0", docs_url=None)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(authorization_router)
app.include_router(authentication_router)


@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
    detail = [
        {key: error[key] for key in ("loc", "msg", "type")}
        for error in exc.errors()
    ]
    return JSONResponse({"detail": detail}, status_code=422)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Привет, мир!"}


@app.get("/about")
def about_page() -> dict[str, str]:
    return {"name": "Мой блог", "version": "1.0"}


install_docs(app)
