from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from service.firebase_service import create_user, login_user
from fastapi.responses import RedirectResponse
from firebase_admin import auth
from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup/save")
async def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    result = await create_user(email, password, name)
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

