from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

# for testing 
def gen_ai_basic_search(contents,thread):
    apikey = os.getenv("GEN_AI_API_KEY")  
    if not apikey:
        return "Error: API Key is missing!"
    try:
        llm = ChatGoogleGenerativeAI(api_key=SecretStr(apikey), model="gemini-1.5-flash")
        result = llm.invoke(contents)
        return result.content if result else "Error: AI response empty!"
    except Exception as e:
        return f"Error: {str(e)}"
    
def gen_ai_web_search(contents, thread):
    pass

def gen_ai_pro_search(contents, thread):
    pass

def gen_ai_deep_search(contents, thread):
    pass

def gen_ai_pdf_search(contents, thread):
    pass

def open_ai_web_search(contents, thread):
    pass

def open_ai_pro_search(contents, thread):
    pass

def open_ai_deep_search(contents, thread):
    pass

def open_ai_pdf_search(contents, thread):
    pass

def grok_ai_web_search(contents, thread):
    pass

def grok_ai_pro_search(contents, thread):
    pass

def grok_ai_deep_search(contents, thread):
    pass

def grok_ai_pdf_search(contents, thread):
    pass

def deepseek_ai_web_search(contents, thread):
    pass

def deepseek_ai_pro_search(contents, thread):
    pass

def deepseek_ai_deep_search(contents, thread):
    pass

def deepseek_ai_pdf_search(contents, thread):
    pass