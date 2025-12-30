from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import get_ai_response   # ← اسم فایل API خودت را بگذار

app = FastAPI()

# اجازه دسترسی از فرانت React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    prompt: str

@app.post("/generate")
def generate_response(data: UserMessage):
    reply = get_ai_response(data.prompt)
    return {"response": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)