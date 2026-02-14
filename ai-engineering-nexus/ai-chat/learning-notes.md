In your current models.py, you probably have os.getenv('GOOGLE_API_KEY'). If you misspell that key in your .env file, os.getenv just returns None, and your app crashes only when someone tries to chat.

With Pydantic, the app won't even start if a required variable is missing. It acts as a "Gatekeeper."

That's right! SSE (Server-Sent Events) is inherently more resilient for one-way streams because the browser's EventSource API is designed to automatically attempt to reconnect if the connection is interrupted. 📡

In contrast, with WebSockets, if the connection drops, the socket enters a "closed" state, and you usually have to write custom JavaScript logic to detect the drop and initiate a new handshake.

Unlike WebSockets, where you have to catch WebSocketDisconnect, StreamingResponse is a bit more hands-off. However, if the user closes the tab mid-stream, the generator will simply stop yielding. To be extra safe, you can wrap the async for in a try/finally block to perform any cleanup (like logging the end of a session).

🏗️ Why this is perfect for your WebSocket
In your while True loop, the code looks like this:

```Python
while True:
    # Point A: Wait for user input
    question = await websocket.receive_text() 
    
    # Point B: Schedule the AI
    asyncio.create_task(process_ai(question)) 
    
    # Point C: The loop immediately cycles back to Point A.
    # Because 'receive_text()' is an AWAIT, it yields control.
    # THE AI TASK STARTS NOW!

```

The active_tasks[websocket].cancel() Magic
When you call .cancel(), it's not a suggestion; it's a command.

The Injection: Python finds the next await point in that specific task (usually await websocket.send_json(...) or await asyncio.sleep(...)).

The Error: It raises an asyncio.CancelledError.

The Stop: The AI loop stops immediately because it wasn't expecting an error. The task is then destroyed, and the memory is freed.

🏛️ REST vs. WebSocket Analysis (Day 5)
As we wrap up Week 2, we need to document exactly when to use these tools for JARVIS-X. You’ve built both, so now you have the "wisdom" to choose.

| Protocol | Best For... | Biggest Weakness |
| --- | --- | --- |
| REST (Standard) | Fetching history, profile updates, small settings. | No real-time feedback; feels "slow" for AI. |
| SSE (Streaming) | Simple Q&A where the user just waits for the answer. | One-way only; user can't "stop" the AI easily. |
| WebSocket | Complex agents that need to interrupt, or voice/chat apps. | Harder to scale (requires "sticky sessions" or Redis). |

🧊 Learning: The Battery "Saving" Logic
In a mobile world, the most expensive resource (in terms of power) is the Cellular Radio. Every time the radio has to "wake up" to send or receive data, it drains a significant amount of battery.

Why SSE wins on Mobile:
Standard HTTP Efficiency: Because SSE is built on standard HTTP/1.1 or HTTP/2, mobile operating systems (iOS and Android) can optimize the connection. They can "batch" the incoming data or even offload the connection management to a system-level process.

Unidirectional Calm: WebSockets are "full-duplex," meaning the radio has to be ready to send and receive at any millisecond. This keeps the radio in a high-power state. SSE is like a one-way street; the phone can often put its transmitter to sleep and only wake up the receiver when a token arrives.

The "Push Proxy" Effect: Modern mobile browsers can sometimes hand off an SSE connection to a network proxy. The phone goes to "deep sleep," and the proxy wakes it up only when the AI actually has something to say.