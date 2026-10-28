FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG APP_FILE=app.py

COPY ${APP_FILE} /app/app.py

EXPOSE 5000

CMD ["python", "app.py"]