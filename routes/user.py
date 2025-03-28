from fastapi import APIRouter, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from service.firebase_service import create_user, login_user
from fastapi.responses import RedirectResponse
from firebase_admin import auth
from fastapi import APIRouter, HTTPException
from models.ApiDatabase import APIKeys
from service.firebase_service import db
from service.llm import gen_ai


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/user/{user_id}")
def get_user(user_id: str):
    try:
        user = auth.get_user(user_id)
        return {"display_name": user.display_name}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/user/{user_id}/chat", response_class=HTMLResponse)
async def chat_page(user_id: str, request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "user_id": user_id})

@router.get("/user/{user_id}/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user_id: str):
    return templates.TemplateResponse("profile.html", {"request": request, "user_id": user_id})

@router.post("/store-api-keys")
async def store_api_keys(
    user_id: str = Form(...),
    openai_key: str = Form(...),
    grok_key: str = Form(...),
    deepseek_key: str = Form(...),
    google_key: str = Form(...)
):
    try:
        Api_db = db.collection("api_keys").document(user_id)
        
        Api_db.set({
            "openai_key": openai_key,
            "grok_key": grok_key,
            "deepseek_key": deepseek_key,
            "google_key": google_key
        })

        return RedirectResponse(url=f"/user/{user_id}/profile", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/prompt")
async def get_prompt(
    message: str = Form(...),
    file: UploadFile = File(None),
    model: str = Form(...),
    search: str = Form(...)
):
    file_info = {
        "file_name": file.filename if file else "No file uploaded",
        "file_content_type": file.content_type if file else "None"
    }
    ai_response = gen_ai(message)
    return JSONResponse(content={"user_message": message, "ai_response": ai_response})


