FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY experiments ./experiments

CMD ["uvicorn","experiments.ch17_final_cloud_platform.api.app:app","--host","0.0.0.0","--port","8000"]