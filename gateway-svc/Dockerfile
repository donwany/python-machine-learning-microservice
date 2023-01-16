FROM python:3.10.0-slim-bullseye
ENV PYTHONUNBUFFERED 1
WORKDIR /gateway
COPY requirements.txt /gateway
RUN pip install -r requirements.txt
COPY . /gateway
EXPOSE 1958
CMD ["python3", "api.py"]