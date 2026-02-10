import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
from models import get_model_stream
import logging
logger = logging.getLogger("uvicorn") # Hooks into FastAPI's default logger

app = FastAPI()

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
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                const msg = JSON.parse(event.data);
                if (msg.type === "start") {
                    // Create the new list item once
                    currentMessageElement = document.createElement('li');
                    messages.appendChild(currentMessageElement);
                } else if(msg.type === "thinking"){
                    // Append text to the SAME list item
                    currentMessageElement = document.createElement('li');
                    messages.appendChild(currentMessageElement);
                    currentMessageElement.textContent += msg.data;
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
    # Instead of print()
    logger.info("New connection established")
    try:
        while True:
            question = await websocket.receive_text()
            try:
                question_dict = json.loads(question)
                model = question_dict['model']
                question = question_dict['question']
            except json.JSONDecodeError:
                model = "gemini-2.5-flash"
                question = question
            try:
                await websocket.send_json({"type": "start"})
                async for token in get_model_stream(model, question):
                    await websocket.send_json({"type": "content", "data": token})
            except Exception as e:
                await websocket.send_json({"type": "error", "data": "AI is sleepy. Try again!"})
    except WebSocketDisconnect:
        logger.error(f"Client Disconnected!")
