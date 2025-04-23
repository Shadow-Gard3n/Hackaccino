# ☕ Hackaccino – Research-Based AI Toolkit

**Hackaccino** is an AI-powered web application designed to help users perform research more efficiently by leveraging LLMs (Large Language Models) and search tools. The platform is currently under development and offers a fully functional frontend built with FastAPI, with backend features actively being integrated.

> 🔍 Powered by LangChain, Firebase, and FastAPI  
> 🔐 Authentication via Firebase  
> 📚 Modular search tools: Web, Deep, PDF, Pro, and more

---

## 👥 Team

**Team Name:** The Boys

**Team Members:**
- Aryan Gahlot  
- Lakhan Gupta  
- Yash Mittal  
- Vivek  
- Tarush Saxena  

---

## 🚧 Project Status

> ✅ Frontend: Complete

> ✅ Database & Routes (Auth): Complete

> ⚙️ LLM Integration (Response Handling): In Progress

---

## 📸 Screenshots

<!-- First Image -->
<img src="https://github.com/user-attachments/assets/014d176f-225c-4357-bdd4-3df2925a2ba5" width="400"/>

<!-- Second Image -->
<img src="https://github.com/user-attachments/assets/51990848-8851-40f4-95c2-672ee1761b68" width="600"/>


---

## 🧠 Features

- 🔐 **User Authentication** – Login & Signup via Firebase Auth
- 🧪 **AI-Based Research** – Multiple search modes powered by LangChain and external APIs
  - 🔍 Web Search
  - 🧠 Deep Search
  - 📄 PDF Search
  - 🧑‍🔬 Pro Search
- 📦 Modular integration for various AI backends:
  - Google Generative AI
  - OpenAI
  - DeepSeek
  - Grok AI
- 🧩 Extensible API structure using FastAPI routers

---

## 🛠️ Tech Stack

| Frontend        | Backend              | AI/ML               | Auth & DB          |
|-----------------|----------------------|---------------------|--------------------|
| HTML + Jinja2   | FastAPI              | LangChain           | Firebase Auth      |
| CSS             | Python (3.10+)       | Google GenAI        | Firestore Database |
| JavaScript      | REST API (FastAPI)   | OpenAI, DeepSeek AI |                    |

---

## 📁 Project Structure

```bash
Hackaccino/
│
├── main.py                        # FastAPI main entry point
├── routes/
│   ├── auth.py                    # Firebase auth routes
│   └── user.py                    # User route logic
│
├── service/
│   ├── firebase_service.py       # Firebase helper functions
│   └── llm.py                    # LangChain + LLM integrations
│
├── models/
│   └── ApiDatabase.py            # Pydantic model for API keys
│
├── templates/                    # Jinja2 HTML templates
├── static/                       # Static files (CSS, JS, images)
├── .env                          # Environment variables
└── README.md                     # Project documentation
```


## To run use these commands
```
git clone https://github.com/Shadow-Gard3n/Hackaccino.git
cd Hackaccino
pip install fastapi uvicorn python-dotenv firebase-admin requests langchain langchain-google-genai google-auth jinja2 pydantic
uvicorn main:app --reload

