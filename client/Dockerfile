FROM python:3.9-slim

WORKDIR /app

RUN pip install aiohttp

COPY client/client.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "client.py"]