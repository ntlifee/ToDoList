FROM python:3.13.0-alpine3.20

WORKDIR /app

COPY /requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY db.py .
COPY model_task.py .
COPY schemas_task.py .
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
