FROM python:3.10.0-slim-bullseye
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["python3", "app.py"]