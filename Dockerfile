FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# устанавливаем Chromium для Playwright
RUN playwright install chromium

COPY . .

# Запуск через shell-форму для корректной подстановки переменных среды
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
