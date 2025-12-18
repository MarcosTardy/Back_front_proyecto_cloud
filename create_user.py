from database import SessionLocal
from models import User
from security import hash_password  # o donde tengas esta función

def create_user():
    db = SessionLocal()

    user = User(
        username="admin",
        password_hash=hash_password("12345678")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("Usuario admin creado con ID:", user.id)

    db.close()
if __name__ == "__main__":
    create_user()