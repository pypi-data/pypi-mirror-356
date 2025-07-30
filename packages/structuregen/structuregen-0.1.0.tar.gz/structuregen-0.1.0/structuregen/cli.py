import os

STRUCTURE = [
    "server/app/api/v1/routes/users.py",
    "server/app/api/v1/routes/documents.py",
    "server/app/api/v1/routes/search.py",
    "server/app/api/v1/__init__.py",
    "server/app/api/__init__.py",

    "server/app/core/config.py",
    "server/app/core/security.py",
    "server/app/core/__init__.py",

    "server/app/db/base.py",
    "server/app/db/session.py",
    "server/app/db/models/user.py",
    "server/app/db/models/paper.py",
    "server/app/db/models/__init__.py",
    "server/app/db/__init__.py",

    "server/app/services/embedding.py",
    "server/app/services/document_processor.py",
    "server/app/services/graph_builder.py",
    "server/app/services/__init__.py",

    "server/app/schemas/user.py",
    "server/app/schemas/document.py",
    "server/app/schemas/__init__.py",

    "server/app/utils/file.py",
    "server/app/utils/logger.py",
    "server/app/utils/__init__.py",

    "server/app/main.py",
    "server/app/__init__.py",

    "server/tests/conftest.py",
    "server/tests/test_users.py",
    "server/tests/test_documents.py",

    "server/alembic/",
    "server/.env",
    "server/requirements.txt",
    "server/gunicorn_conf.py",
    "server/Dockerfile"
]

def generate_structure():
    for path in STRUCTURE:
        if path.endswith("/"):
            os.makedirs(path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                pass
    print("✅ Project structure generated under 'server/'.")

if __name__ == "__main__":
    generate_structure()
