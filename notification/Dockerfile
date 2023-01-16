FROM python:3.10.9-slim-bullseye

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

CMD ["python3", "app.py"]