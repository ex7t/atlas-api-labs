from fastapi import FastAPI

from src.routers.post_router import router as post_router

from web.docs import install_docs

app = FastAPI(title="Мой блог", version="1.0", docs_url=None)
app.include_router(post_router)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Привет, мир!"}


@app.get("/about")
def about_page() -> dict[str, str]:
    return {"name": "Мой блог", "version": "1.0"}


install_docs(app)
