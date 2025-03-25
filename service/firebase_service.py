# import firebase_admin
# from firebase_admin import auth, credentials

# cred = credentials.Certificate("D:\\Coding\\web with python\\FastApi\\project\\serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# async def create_user(email: str, password: str):
#     try:
#         user = auth.create_user(email=email, password=password)
#         return {"status": "User created successfully", "user_id": user.uid}
#     except Exception as e:
#         return {"error": str(e)}

# async def login_user(email: str, password: str):
#     try:
#         return {"message": "Verify using Firebase client-side SDK."}
#     except Exception as e:
#         return {"error": str(e)}


import firebase_admin
from firebase_admin import auth, credentials
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("D:\\Coding\\web with python\\FastApi\\project\\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

FIREBASE_API_KEY = "AIzaSyAndM9OxoBzQE9ap0YCEuPvBGnNmNM7Ayw"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

async def create_user(email: str, password: str):
    try:
        user = auth.create_user(email=email, password=password)
        return {"status": "User created successfully", "user_id": user.uid}
    except Exception as e:
        return {"error": str(e)}

async def login_user(email: str, password: str):
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_SIGNIN_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            return {
                "message": "Login successful",
                "idToken": data["idToken"],      
                "refreshToken": data["refreshToken"], 
                "userId": data["localId"]
            }
        else:
            return {"error": response.json().get("error", {}).get("message", "Login failed")}
    except Exception as e:
        return {"error": str(e)}
