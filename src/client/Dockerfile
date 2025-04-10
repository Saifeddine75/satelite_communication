FROM python:3.9-slim

WORKDIR /src

RUN pip install aiohttp

COPY src/client/client.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "client.py"]