# AI Q&A

An intelligent question-and-answer API built with FastAPI that leverages Google's Gemini AI model for both one-off queries and conversational chat with memory persistence.

## Features

- **Streaming Responses**: Real-time AI responses using Server-Sent Events (SSE)
- **Stateless Q&A**: Single-turn question answering via `/ask` endpoint
- **Conversational Chat**: Multi-turn conversations with session-based memory via `/chat` endpoint
- **Session Management**: Cookie-based session tracking for personalized chat history
- **Memory Persistence**: Redis-backed chat history storage with automatic expiration
- **Google Gemini Integration**: Powered by Gemini 2.5 Flash model

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Client    │─────▶│   FastAPI    │─────▶│  Gemini API     │
│  (Browser)  │◀─────│   Server     │◀─────│  (via OpenAI)   │
└─────────────┘ SSE  └──────────────┘      └─────────────────┘
                            │
                            ▼
                      ┌──────────────┐
                      │    Redis     │
                      │ (Chat Memory)│
                      └──────────────┘
```

## Prerequisites

- Python 3.12 or higher
- Redis server (for chat memory)
- Google API Key (Gemini access)

## Installation

1. **Clone the repository**
   ```bash
   cd ai-engineering-nexus/ai-qna
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   
   Create a `.env` file in your project root with:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Start Redis server**
   ```bash
   redis-server
   ```

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Endpoints

#### Health Check
```http
GET /health
```
Returns server health status.

#### Single-Turn Q&A (Streaming)
```http
POST /ask?question=Your+question+here
```
Streams the AI response in real-time without maintaining conversation history.

**Example:**
```bash
curl -N "http://127.0.0.1:8000/ask?question=What%20is%20artificial%20intelligence?"
```

#### Conversational Chat
```http
POST /chat?message=Your+message+here
```
Maintains conversation context using session cookies. Chat history is stored in Redis and expires after 1 hour.

**Example:**
```bash
curl -X POST -b cookies.txt -c cookies.txt \
  "http://127.0.0.1:8000/chat?message=Hello,%20my%20name%20is%20John"

curl -X POST -b cookies.txt -c cookies.txt \
  "http://127.0.0.1:8000/chat?message=What%20is%20my%20name?"
```

### Interactive API Documentation

FastAPI provides auto-generated interactive docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Technical Details

### Session Management
- Sessions are identified by UUID v4 tokens stored in browser cookies
- Cookie lifetime: 3600 seconds (1 hour)
- Each session maintains its own isolated chat history

### Memory Storage
- Chat history stored in Redis with key format: `chat:{session_id}`
- Automatic expiration: 3600 seconds (1 hour)
- Format: JSON array of message objects with `role` and `content`

### Streaming Architecture
- Uses SSE (Server-Sent Events) for real-time response streaming
- Supports client disconnection handling to avoid wasted API calls
- Chunk-by-chunk content delivery for better UX

## Dependencies

- **fastapi[standard]** - Web framework and server
- **openai** - Client for Gemini API (OpenAI-compatible endpoint)
- **redis** - Async Redis client for session storage
- **sse-starlette** - Server-Sent Events support
- **python-dotenv** - Environment variable management

## Project Structure

```
ai-qna/
├── main.py                 # FastAPI application and endpoints
├── pyproject.toml          # Project dependencies and metadata
├── README.md               # This file
└── learning-notes.md       # Development notes and learnings
```

## Development Notes

- Async/await used throughout for optimal I/O performance
- Redis client configured for async operations with `decode_responses=True`
- Environment-specific .env path (update as needed for production)
- Model: `gemini-2.5-flash` (configurable)

## Future Enhancements

- [ ] Add authentication and user management
- [ ] Implement conversation export/import
- [ ] Add support for multiple AI models
- [ ] Rate limiting and usage analytics
- [ ] Vector database integration for RAG capabilities
- [ ] WebSocket alternative to SSE
- [ ] Docker containerization

## License

This project is part of the AI Engineering Nexus learning repository.

## Author

Developed as part of AI engineering studies and hands-on learning.
