FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /project/pyproject.toml

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic-settings

COPY apps/api/app ./app
COPY experiments/__init__.py ./experiments/__init__.py
COPY experiments/ch08_infrastructure ./experiments/ch08_infrastructure
COPY experiments/ch09_specialized_mechanisms ./experiments/ch09_specialized_mechanisms

EXPOSE 8000

CMD [ "uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
