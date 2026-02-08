from fastapi import FastAPI, Request, Response, Depends
import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from sse_starlette.sse import EventSourceResponse
import uuid
import json
from redis.asyncio import Redis

load_dotenv(r'C:\Users\SRJ\SRJ\Work\agentic_ai\.env')

app = FastAPI()

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

gemini_api_key = os.getenv('GOOGLE_API_KEY')

openai = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model="gemini-2.5-flash"

@app.get("/")
def home():
    return {"status": "running", "manager": "uv", "server": "uvicorn"}

@app.get("/health")
def health():
    return {"status": "healthy"}

async def get_answer(question: str, request: Request):
    response = await openai.chat.completions.create(
        model=model,
        messages=[
            {   "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Answer this question: {question}"
            }
        ],
        stream = True
    )
    async for chunk in response:
        if await request.is_disconnected():
            break
        content = chunk.choices[0].delta.content
        if content:
            yield {"data" : content}

@app.post("/ask")
async def ask(question: str, request: Request):
    return EventSourceResponse(get_answer(question, request))

async def get_answer_from_memory(message: str, request: Request, response: Response):
    session_id = request.cookies.get('session_id')

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, max_age=3600)

    print(f'session_id : {session_id}')

    messages=[
        {   "role": "system",
            "content": "You are a helpful assistant. You keep a history of chat and answer questions."
        }
    ]

    raw_data = await redis_client.get(f"chat:{session_id}")
    history = json.loads(raw_data) if raw_data else []

    print(f'History: {history}')

    if history:
        messages.extend(history)
    
    messages.append({"role": "user", "content": message})

    print(f'messages : {messages}')

    response = await openai.chat.completions.create(
        model=model,
        messages=messages
    )

    print(f'response : {response}')

    assistant_response = response.choices[0].message.content

    print(f'assistant_response : {assistant_response}')

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": assistant_response})

    await redis_client.setex(f"chat:{session_id}", 3600, json.dumps(history))

    print(f'history : {history}')

    return assistant_response

@app.post("/chat")
async def chat(message: str, request: Request, response: Response):
    print(f'message : {message}')
    return await get_answer_from_memory(message, request, response)
