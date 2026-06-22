python -m venv venv 
./venv/Scripts/Activate.ps1 # Для Windows

pip install fastapi             # Установка фреймворка FastAPI 
pip install "uvicorn[standard]" # Установка ASGI-сервера 
pip install alembic             # Средство для миграций БД 
pip install pydantic-settings   # Модуль для управления конфигурацией сервиса 
pip install aio_pika            # Модуль для асинхронной работы с RabbitMQ 



pip install opentelemetry-distro opentelemetry-exporter-otlp

opentelemetry-bootstrap -a install