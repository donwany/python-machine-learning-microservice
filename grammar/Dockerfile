FROM python:3.10.0-slim-bullseye

RUN apt update -y &&  \
    apt-get install -y software-properties-common && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' &&  \
    apt update -y && \
    apt-get install -y openjdk-8-jdk-headless && \
    apt-get clean;

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["python3", "app.py"]