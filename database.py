from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "users-db.cv00cokek7v1.eu-north-1.rds.amazonaws.com"
DB_NAME = "users-db"
DB_PORT = 5432

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
# Esto crea todas las tablas que están definidas en Base
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente")