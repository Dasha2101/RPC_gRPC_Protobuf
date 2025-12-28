FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY glossary ./glossary

EXPOSE 50053

CMD ["python", "-m", "glossary.glossary_server"]
