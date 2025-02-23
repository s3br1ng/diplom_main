from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Настройки подключения к базе данных
DATABASE_URL = "sqlite:///./test.db"

# Создание движка базы данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()