# Указываем базовый образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Копируем файл с зависимостями и устанавливаем их
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем остальные файлы проекта в контейнер
COPY . .

# Определяем переменные окружения
ENV DEBUG=True

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Создаем директорию для статики
RUN mkdir -p /app/staticfiles

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
