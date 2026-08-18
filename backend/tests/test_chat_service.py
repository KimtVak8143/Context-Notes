from app.services.chat_service import build_context_prompt, generate_reply


def test_build_context_prompt_includes_note_context():
    notes = [
        {"title": "Alpha", "content": "Summary of alpha"},
        {"title": "Beta", "content": "Summary of beta"},
    ]

    prompt = build_context_prompt("What did I write about alpha?", notes)

    assert "Alpha" in prompt
    assert "Summary of alpha" in prompt
    assert "What did I write about alpha?" in prompt


def test_generate_reply_uses_openai_when_key_present(monkeypatch):
    captured = {}

    class FakeClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    captured.update(kwargs)
                    return type("Resp", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": "Here is your answer."})()})()]})()

    monkeypatch.setattr("app.services.chat_service.OpenAI", lambda api_key=None: FakeClient())
    monkeypatch.setattr("app.services.chat_service.os.getenv", lambda key, default=None: {
        "OPENAI_API_KEY": "sk-test",
        "OPENAI_MODEL": "gpt-4o-mini",
    }.get(key, default))

    reply = generate_reply("Summarize my notes")

    assert reply == "Here is your answer."
    assert captured["model"] == "gpt-4o-mini"


def test_generate_reply_uses_ollama_when_available(monkeypatch):
    captured = {}

    def fake_chat(**kwargs):
        captured.update(kwargs)
        return {"message": {"content": "Here is your answer."}}

    monkeypatch.setattr("app.services.chat_service.ollama.chat", fake_chat)
    monkeypatch.setattr("app.services.chat_service.os.getenv", lambda key, default=None: {
        "OPENAI_API_KEY": "",
        "OLLAMA_MODEL": "llama3.2",
    }.get(key, default))

    reply = generate_reply("Summarize my notes")

    assert reply == "Here is your answer."
    assert captured["model"] == "llama3.2"
