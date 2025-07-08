FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# устанавливаем Chromium для Playwright
RUN playwright install chromium

COPY . .

# Запуск через shell-форму для корректной подстановки переменных среды
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
