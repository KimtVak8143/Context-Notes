import os
from types import SimpleNamespace
from typing import Any, Dict, List

try:
    import ollama
except ImportError:  # pragma: no cover - exercised via fallback behavior
    def _missing_ollama_chat(*_: Any, **__: Any) -> Any:
        raise RuntimeError("The ollama package is not installed.")

    ollama = SimpleNamespace(chat=_missing_ollama_chat)
from openai import OpenAI

from . import note_service


DEFAULT_MODEL = "llama3.2"
DEFAULT_HOST = "http://localhost:11434"


def _get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)


def _get_ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", DEFAULT_HOST)


def _get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def build_context_prompt(user_message: str, notes: List[Dict[str, Any]]) -> str:
    if not notes:
        return f"User message: {user_message}\n\nYou have no saved notes yet. Reply naturally and ask if they'd like to save something."

    formatted = "\n\n".join(
        f"- Title: {note.get('title', 'Untitled')}\n  Content: {note.get('content', '') or 'No content'}\n  Tags: {', '.join(note.get('tags', []) or [])}"
        for note in notes
    )
    return (
        "Use the user's saved notes as context when answering. "
        "Do not invent notes that are not present.\n\n"
        f"User message: {user_message}\n\nSaved notes:\n{formatted}"
    )


def _call_openai(prompt: str) -> str:
    api_key = _get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=_get_openai_model(),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def _call_ollama(prompt: str) -> str:
    response = ollama.chat(
        model=_get_ollama_model(),
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2},
        host=_get_ollama_host(),
    )
    return response["message"]["content"]


def generate_reply(user_message: str, notes: List[Dict[str, Any]] | None = None) -> str:
    if notes is None:
        notes = note_service.list_notes()

    prompt = build_context_prompt(user_message, notes)
    api_key = _get_openai_api_key()

    try:
        if api_key:
            return _call_openai(prompt)
        return _call_ollama(prompt)
    except Exception:
        if api_key:
            return "I couldn't reach the OpenAI API. Please check your API key and network connection."
        return "I couldn't reach the local Ollama service. Please make sure Ollama is running and the model is available."
