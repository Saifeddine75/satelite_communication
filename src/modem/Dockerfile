FROM python:3.9-slim

WORKDIR /src

RUN pip install fastapi uvicorn

COPY src/modem/modem.py .

EXPOSE 8000 8001 8002 

CMD ["python", "modem.py"]