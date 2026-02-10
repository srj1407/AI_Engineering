import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from config import settings

gemini_api_key = settings.google_api_key
openrouter_api_key = settings.openrouter_api_key

gemini = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

openai = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

async def get_model_stream(model: str, question: str):
    if model not in ["gemini-2.5-flash", "openai/gpt-oss-20b:free"]:
        model = settings.default_model
    if model == "gemini-2.5-flash":
        response = await gemini.chat.completions.create(
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
    else:
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
        if chunk:
            yield chunk.choices[0].delta.content