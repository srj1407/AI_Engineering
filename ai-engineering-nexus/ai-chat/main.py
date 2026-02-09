import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
import json

load_dotenv(r'C:\Users\SRJ\SRJ\Work\agentic_ai\.env')

app = FastAPI()

gemini_api_key = os.getenv('GOOGLE_API_KEY')

openai = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model="gemini-2.5-flash"

# This is just a simple UI to test your websocket
html = """
<!DOCTYPE html>
<html>
    <body>
        <h1>WebSocket Echo</h1>
        <input type="text" id="messageText" autocomplete="off"/>
        <button onclick="sendMessage()">Send</button>
        <ul id='messages'></ul>
        <script>
            let currentMessageElement;
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                const msg = JSON.parse(event.data);
                if (msg.type === "start") {
                    // Create the new list item once
                    currentMessageElement = document.createElement('li');
                    messages.appendChild(currentMessageElement);
                } else {
                    // Append text to the SAME list item
                    currentMessageElement.textContent += msg.data;
                } 
            };
            function sendMessage() {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

# YOUR TASK: Implement the @app.websocket("/ws") route here
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            question = await websocket.receive_text()
            try:
                await websocket.send_json({"type": "thinking", "data": "Thinking..."})
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
                await websocket.send_json({"type": "start"})
                async for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        await websocket.send_json({"type": "content", "data": content})
            except Exception as e:
                await websocket.send_json({"type": "error", "data": "AI is sleepy. Try again!"})


    except WebSocketDisconnect:
        print('Client disconnected')
