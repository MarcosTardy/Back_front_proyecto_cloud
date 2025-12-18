from database import SessionLocal
from models import User
from main import hash_password  # o donde tengas esta función

def create_user():
    db = SessionLocal()

    user = User(
        username="admin",
        password_hash=hash_password("12345678")
    )

    db.add(user)
    db.commit()

    print("Usuario admin creado")

    db.close()