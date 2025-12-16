from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "users-db.cv00cokek7v1.eu-north-1.rds.amazonaws.com"
DB_NAME = "users-db"
DB_PORT = 5432

#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = "postgresql://usuario:contraseña@users-db.cv00cokek7v1.eu-north-1.rds.amazonaws.com:5432/users-db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
db = SessionLocal()
    
# Esto crea todas las tablas que están definidas en Base

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

user1 = User(username="admin", password_hash=hash_password("12345678"))
#user2 = User(username="marcos", password_hash=hash_password("123"))
#user3 = User(username="besiter", password_hash=hash_password("321"))
#user4 = User(username="kira", password_hash=hash_password("321"))
#user5 = User(username="titi", password_hash=hash_password("123"))

db.add(user1)
db.commit()
db.refresh(user1)

Base.metadata.create_all(bind=engine)