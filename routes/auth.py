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
    error = request.query_params.get("error", "")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    error = request.query_params.get("error", "")
    return templates.TemplateResponse("signup.html", {"request": request, "error": error})

@router.post("/signup/save")
async def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    result = await create_user(email, password, name)
    
    if "error" in result:
        error_message = result["error"]
               
       
        if "INVALID_EMAIL" in error_message:
            error_message = "Invalid email address. Please try with valid email."
        elif "Invalid password string" in error_message:
            error_message = "Invalid password. Password must be a string at least 6 characters long."
        elif "EMAIL_EXISTS" in error_message:
            error_message = "The email is already registered. Try logging in."
        else:
            error_message = result["error"]
        
        return RedirectResponse(url=f"/signup?error={error_message}", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@router.post("/login/save")
async def login(email: str = Form(...), password: str = Form(...)):
    result = await login_user(email, password)
    
    if "error" in result:
        error_message = result["error"]
        if "INVALID_LOGIN_CREDENTIALS" in error_message:
            error_message = "Invalid email or password. Please try again."
        else:
            error_message = result["error"]
            
        return RedirectResponse(url=f"/login?error={error_message}", status_code=303)

    user_id = result.get("userId")
    session_token = result.get("idToken", "") 

    if not session_token:
        return RedirectResponse(url="/login?error=InvalidSession", status_code=303)  # handle missing session token

    response = RedirectResponse(url=f"/user/{user_id}/chat", status_code=303)
    response.set_cookie(key="session", value=session_token, httponly=True, max_age=604800)  # store session securely
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session")  # Remove session cookie
    return response
