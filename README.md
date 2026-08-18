# Context — Notes App

A lightweight notes app with a FastAPI backend, MongoDB persistence, and a pastel Next.js frontend.

## Requirements

- Node.js 18+
- Python 3.12+
- MongoDB 7.x, or Docker/Podman with Compose
- Optional: OpenAI API key for the AI note Q&A feature

## Quick start

### 1) Configure environment

Copy the example env file and update values as needed:

```bash
cd context
cp .env.example .env
```

For the backend runtime, the app loads `backend/.env` directly. If needed, create it with values like:

```bash
cd context/backend
cp .env.example .env
```

Example values:

```env
MONGODB_URI=mongodb://localhost:27017/context
MONGODB_DB=context
USE_IN_MEMORY_DB=false
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
```

### 2) Start MongoDB

Using Docker Compose:

```bash
cd context
docker compose up -d mongo
# or: podman compose up -d mongo
```

### 3) Start the backend

```bash
cd context/backend
python3 run.py
```

The API is available at:

- Backend: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- MongoDB: mongodb://localhost:27017/context

### 4) Start the frontend

```bash
cd context/frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

## Full stack with compose

```bash
cd context
make up
```

This starts the MongoDB, backend, and frontend together.

## Useful commands

```bash
cd context
make backend-run
make frontend-dev
make backend-test
make down
```

## Architecture notes

- The backend uses MongoDB for persistence and exposes REST endpoints under `/api/v1`.
- The app keeps business logic in a `note_service` layer so the API and future integrations can reuse the same behavior.
- The AI chat route is note-aware and prefers OpenAI when an API key is present, with Ollama as a fallback.
- The frontend is intentionally small and clean, with a note editor pane and a note list, plus an AI ask-notes panel.

## Troubleshooting

- If the backend fails to start, confirm MongoDB is running and the backend environment file is present.
- If the backend is started from the wrong directory, Python may not find the app module; use `cd context/backend && python3 run.py`.
- If the app cannot reach MongoDB, verify `MONGODB_URI` and ensure `USE_IN_MEMORY_DB=false` unless you are intentionally testing with in-memory storage.
