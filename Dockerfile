FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY data /app/data

EXPOSE 9004

CMD ["python", "src/app.py"]