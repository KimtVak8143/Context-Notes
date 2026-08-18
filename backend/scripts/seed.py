"""Seed the database with example notes for development."""
from app.db.database import SessionLocal, engine, Base
from app.models.note import Note


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        examples = [
            {"title": "Kubernetes Networking", "content": "Notes about Services, CNI and NetworkPolicies.", "tags": ["kubernetes", "networking"]},
            {"title": "AWS ECS Debugging", "content": "Troubleshooting ECS tasks and networking.", "tags": ["aws", "ecs"]},
            {"title": "DevOps Interview Notes", "content": "Common questions and answers.", "tags": ["devops", "interview"]},
            {"title": "AI Project Ideas", "content": "Ideas for AI projects without LLM integration yet.", "tags": ["ai", "ideas"]},
            {"title": "Things to Learn", "content": "List of topics to learn next.", "tags": ["learning"]},
        ]
        for ex in examples:
            note = Note(title=ex["title"], content=ex["content"], tags=ex["tags"])
            db.add(note)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
