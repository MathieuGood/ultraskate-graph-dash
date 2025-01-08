FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9004

CMD ["python3", "src/app.py"]
