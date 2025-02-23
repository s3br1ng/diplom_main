# backend/__init__.py

from .main import app  # Импортируем приложение FastAPI
from .database import engine  # Импортируем движок БД
from .models import Base  # Импортируем модели SQLAlchemy

# Создание таблиц в базе данных при импорте пакета
Base.metadata.create_all(bind=engine)