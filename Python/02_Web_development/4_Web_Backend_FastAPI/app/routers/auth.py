from fastapi import APIRouter, Request, Form, Response
from app.users_db import create_user, get_user, verify_password, delete_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from starlette.config import Config


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if user and verify_password(password, user["password"]):
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie("username", username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "로그인 실패"})


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("username")
    return response


@router.post("/register", response_class=HTMLResponse)
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    create_user(username, password)
    #if user_exists(username):
    #    return templates.TemplateResponse("popup.html", {
    #        "request": request,
    #        "message": "이미 존재하는 사용자입니다.",
    #        "redirect_url": "/register"
    #    })

    create_user(username, password)
    return templates.TemplateResponse("popup.html", {
        "request": request,
        "message": "회원가입이 완료되었습니다.",
        "redirect_url": "/login"
    })


@router.post("/delete")
def delete(username: str = Form(...)):
    delete_user(username)
    return {"msg": "삭제 완료"}

config_data = {
    "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
    "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
    "OKTA_CLIENT_ID": os.getenv("OKTA_CLIENT_ID"),
    "OKTA_CLIENT_SECRET": os.getenv("OKTA_CLIENT_SECRET"),
    "OKTA_DOMAIN": os.getenv("OKTA_DOMAIN"),
}

### OAuth & Okta

config = Config(environ=config_data)
oauth = OAuth(config)

# Google 등록
oauth.register(
    name='google',
    client_id=config_data["GOOGLE_CLIENT_ID"],
    client_secret=config_data["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Okta 등록
oauth.register(
    name='okta',
    client_id=config_data["OKTA_CLIENT_ID"],
    client_secret=config_data["OKTA_CLIENT_SECRET"],
    server_metadata_url=f"https://{config_data['OKTA_DOMAIN']}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"user": user_info}


@router.get("/auth/okta")
async def login_okta(request: Request):
    redirect_uri = request.url_for("auth_okta_callback")
    return await oauth.okta.authorize_redirect(request, redirect_uri)


@router.get("/auth/okta/callback")
async def auth_okta_callback(request: Request):
    token = await oauth.okta.authorize_access_token(request)
    user_info = await oauth.okta.parse_id_token(request, token)
    return {"user": user_info}