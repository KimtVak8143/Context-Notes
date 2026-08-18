"""Run the FastAPI app with Uvicorn via `python3 run.py`."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

if __name__ == "__main__":
    # Import here so environment variables are loaded first
    import uvicorn
    host = os.getenv("HOST") or "127.0.0.1"
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEV", "1") == "1"

    # uvicorn requires an import string (module:app) for reload/workers to work reliably.
    if reload:
        uvicorn.run("app.main:app", host=host, port=port, reload=True)
    else:
        # import the app object directly for production run
        from app.main import app
        uvicorn.run(app, host=host, port=port, reload=False)
