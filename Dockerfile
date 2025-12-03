FROM python:3.11-slim

# Создаём директорию приложения
WORKDIR /app

# Скопировать зависимости заранее (для кеширования)
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Запуск
CMD ["python", "bot.py"]
