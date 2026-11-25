from fastapi import FastAPI

from web.docs import install_docs

app = FastAPI(title="Мой блог", version="1.0", docs_url=None)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Привет, мир!"}


@app.get("/about")
def about_page() -> dict[str, str]:
    return {"name": "Мой блог", "version": "1.0"}


install_docs(app)
