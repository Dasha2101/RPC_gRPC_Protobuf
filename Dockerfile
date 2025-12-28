FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80 50051

CMD ["bash", "-c", "python glossary/server.py & sleep 3 && uvicorn main:app --host 0.0.0.0 --port 80"]
