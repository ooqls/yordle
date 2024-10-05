FROM python:3.12-alpine AS build

COPY backend/app/ /app/
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:api" ]