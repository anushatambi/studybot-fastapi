import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pymongo import MongoClient
from datetime import datetime

SYSTEM_PROMPT = (
    "You are StudyBot, an AI-powered study assistant. "
    "You help students by explaining academic concepts clearly, "
    "step-by-step, in simple language."
)

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB connection
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["studybot"]
collection = db["chats"]

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b"
)

class ChatRequest(BaseModel):
    user_id: str
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
   
    # Fetch last 3 chats for context
    previous_chats = list(
    collection.find({"user_id": request.user_id})
    .sort("created_at", -1)
    .limit(3)
)

    context = SYSTEM_PROMPT + "\n\n"

    if previous_chats:
        context += "Previous conversation:\n"
        for chat in reversed(previous_chats):
            context += f"User: {chat['question']}\n"
            context += f"Bot: {chat['answer']}\n"
        context += "\n"

    context += f"\nUser: {request.question}\nBot:"

    # Get response from LLM
    response = llm.invoke(context).content

    # Store chat for this user
    collection.insert_one({
        "user_id": request.user_id,
        "question": request.question,
        "answer": response,
        "created_at": datetime.utcnow()
    })

    return {"answer": response}