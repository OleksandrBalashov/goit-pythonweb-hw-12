FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ libc-dev libffi-dev libssl-dev \
    && apt-get clean

COPY requirements.txt /app/


RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/

# Команда запуска
CMD ["python3", "main.py"]