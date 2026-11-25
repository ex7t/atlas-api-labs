from html import escape
from pathlib import Path
from string import Template

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

WEB_DIR = Path(__file__).resolve().parent


def install_docs(app: FastAPI) -> None:
    app.mount("/docs-assets", StaticFiles(directory=WEB_DIR / "assets"), name="atlas_assets")
    page = Template((WEB_DIR / "docs.html").read_text(encoding="utf-8"))

    @app.get("/docs", include_in_schema=False)
    async def atlas_docs(request: Request) -> HTMLResponse:
        root = request.scope.get("root_path", "").rstrip("/")
        return HTMLResponse(
            page.substitute(
                assets=escape(f"{root}/docs-assets", quote=True),
                docs=escape(f"{root}/docs", quote=True),
                spec=escape(f"{root}{app.openapi_url}", quote=True),
                redirect=escape(f"{root}/docs/oauth2-redirect", quote=True),
                title=escape(app.title),
                version=escape(app.version),
            )
        )

    @app.get("/docs/oauth2-redirect", include_in_schema=False)
    async def atlas_oauth_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()
