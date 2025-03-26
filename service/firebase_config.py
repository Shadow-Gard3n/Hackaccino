import firebase_admin
from firebase_admin import credentials, firestore
import os

if not firebase_admin._apps:
    cred = credentials.Certificate("D:\\Coding\\web with python\\FastApi\\project\\serviceDatabaseKey.json")  # Path to your Firebase Admin SDK JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()
