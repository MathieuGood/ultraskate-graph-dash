# Use an official Python runtime as a parent image
FROM python:3.12-slim

WORKDIR /src

COPY . /src

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5004

CMD ["python3", "app.py"]