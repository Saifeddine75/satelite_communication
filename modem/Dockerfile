FROM python:3.9-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY modem/modem.py .

EXPOSE 8000 8001 8002 

CMD ["python", "modem.py"]