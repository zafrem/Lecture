from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.routers import auth
from app.routers import internal_page
from starlette.middleware.sessions import SessionMiddleware

description = """
GUI for simple system support.

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Process-Helper",
    description=description,
    summary="Simple Process Support.",
    version="0.0.1",
    terms_of_service="http://127.0.0.1:8000/",
    contact={
        "name": "Simple UI",
        "url": "https://github.com/zafrem/Process-Helper",
        "email": "zafrem@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/document", redoc_url=None
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(internal_page.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("index.html", {"request": request, "username": username})


app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
