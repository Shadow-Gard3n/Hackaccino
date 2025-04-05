from fastapi import APIRouter, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from service.firebase_service import create_user, login_user, get_current_user
from fastapi.responses import RedirectResponse
from firebase_admin import auth
from fastapi import APIRouter, HTTPException
from models.ApiDatabase import APIKeys
from service.firebase_service import db
from service.llm import gen_ai


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/user/me")
async def get_user(request: Request, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        user = auth.get_user(current_user)  # Fetch user using session's user ID
        return {"display_name": user.display_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/user/{user_id}/chat", response_class=HTMLResponse)
async def chat_page(user_id: str, request: Request, current_user: str = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/login", status_code=303)  # redirect only if user is not logged in
    if current_user != user_id:  
        return RedirectResponse(url=f"/user/{current_user}/chat", status_code=303)  # redirect correctly
    return templates.TemplateResponse("chat.html", {"request": request, "user_id": user_id})


@router.get("/user/{user_id}/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user_id: str, current_user: str = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/login", status_code=303)
    if current_user != user_id:  
        return RedirectResponse(url=f"/user/{current_user}/profile", status_code=303)
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
    
data_list = []
@router.post("/prompt")
async def get_prompt(
    message: str = Form(...),
    file: UploadFile = File(None),
    model: str = Form(...),
    search: str = Form(...),
    Depth: str = Form(...),
    button_value: str = Form(...)
):
    file_info = {
        "file_name": file.filename if file else "No file uploaded",
        "file_content_type": file.content_type if file else "None"
    }
    data_list.append(file_info["file_name"])
    ai_response = gen_ai(message)
    print(button_value) #test
    print(model) #test
    print(search) #test
    print(Depth) #test
    return JSONResponse(content={"user_message": message, "ai_response": ai_response, "data_list": data_list})

@router.post("/history/thread")
async def get_thread(request: Request):
    form_data = await request.form() 
    button_value = form_data.get("button_value")

    #need to declare it from llm  
    thread = {"user": ["hi","bye","test"],
              "ai": ["hii", "byee","tesssttt"]}

    print("Button value:", button_value) #test
    return JSONResponse(content={"user_message": thread["user"], "ai_response": thread["ai"]})