from fastapi import FastAPI

app = FastAPI(title="Мой блог", version="1.0")


@app.get("/")
def hello_world() -> dict[str, str]:
    return {"message": "Привет, мир!"}


@app.get("/about")
def about_page() -> dict[str, str]:
    return {"name": "Мой блог", "version": "1.0"}
