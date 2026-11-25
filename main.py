from fastapi import FastAPI

from src.routers.post_router import router as post_router

app = FastAPI(title="Мой блог", version="1.0")
app.include_router(post_router)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Привет, мир!"}


@app.get("/about")
def about_page() -> dict[str, str]:
    return {"name": "Мой блог", "version": "1.0"}


install_docs(app)
