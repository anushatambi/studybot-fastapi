# StudyBot – AI-Powered Study Assistant

StudyBot is an AI-powered chatbot built using FastAPI and a Large Language Model.
It helps students ask study-related questions and remembers previous conversations
using MongoDB.

## Features
- FastAPI-based REST API
- AI responses using Groq LLM
- User-specific conversation memory
- MongoDB for persistent chat storage

## Tech Stack
- Python
- FastAPI
- MongoDB Atlas
- LangChain + Groq
- Uvicorn

## API Endpoint
POST /chat

Example request:
```json
{
  "user_id": "student_1",
  "question": "Explain Newton's First Law"
}
