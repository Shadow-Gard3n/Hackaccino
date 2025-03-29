from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

def gen_ai(contents):
    apikey = os.getenv("GEN_AI_API_KEY")  
    if not apikey:
        return "Error: API Key is missing!"
    try:
        llm = ChatGoogleGenerativeAI(api_key=SecretStr(apikey), model="gemini-1.5-flash")
        result = llm.invoke(contents)
        return result.content if result else "Error: AI response empty!"
    except Exception as e:
        return f"Error: {str(e)}"