from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from service.firebase_service import create_user, login_user
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/user/{user_id}/chat", response_class=HTMLResponse)
async def chat_page(user_id: str, request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "user_id": user_id})

@router.get("/user/{user_id}/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user_id: str):
    return templates.TemplateResponse("profile.html", {"request": request, "user_id": user_id})

@router.post("/signup/save")
async def signup(email: str = Form(...), password: str = Form(...)):
    result = await create_user(email, password)
    if "error" in result:
        return result  
    return RedirectResponse(url="/login", status_code=303)


@router.post("/login/save")
async def login(email: str = Form(...), password: str = Form(...)):
    result = await login_user(email, password)
    if "error" in result:
        return result  
    user_id = result.get("userId")
    return RedirectResponse(url=f"/user/{user_id}/chat", status_code=303)
