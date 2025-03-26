from pydantic import BaseModel

class APIKeys(BaseModel):
    user_id: str
    openai_key: str
    grok_key: str
    deepseek_key: str
    google_key: str
