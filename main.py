from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request, Form, HTTPException, Cookie, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt, JWTError
from fastapi import UploadFile, File
import pandas as pd
from database import SessionLocal, engine, Base
from models import User
from security import hash_password, verify_password

SECRET_KEY = "u2C2mZQ+XdCXTnHntpzsYJ3n8voe28iN7OjzIaUq3iE="
TOKEN_SECONDS_EXP = 3600

app = FastAPI()
Base.metadata.create_all(bind=engine)

jinja2_template = Jinja2Templates(directory="templates")

#Dependencias de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(access_token: Optional[str] = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401)
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=401)
    
def authenticate_user(stored_hash: str, plain_password: str):
    return verify_password(plain_password, stored_hash)

def create_token(data: list):
    data_token = data.copy()
    data_token["exp"] = datetime.now(timezone.utc) + timedelta(seconds = TOKEN_SECONDS_EXP)
    token_jwt = jwt.encode(data_token, key = SECRET_KEY, algorithm = "HS256")
    return token_jwt
    
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return jinja2_template.TemplateResponse("index.html", {"request": request})

@app.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, username: str = Depends(get_current_user)):
    return jinja2_template.TemplateResponse("dashboard.html", {"request": request, "user": username})

@app.post("/users/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="No autorizado")

    token = jwt.encode(
        {
            "username": user.username,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3600)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    response = RedirectResponse("/users/dashboard", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response

    
@app.post("/users/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response

#Para mostrar la pg del equipo 
@app.get("/users/team", response_class=HTMLResponse)
def team_page(request: Request, username: str = Depends(get_current_user)):
    return jinja2_template.TemplateResponse("team.html", {"request": request, "user": username})

#Para recibir y procesar el csv
@app.post("/users/upload_csv")
async def upload_csv(file: UploadFile = File(...)):#, username: str = Depends(get_current_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV")
    df = pd.read_csv(file.file)
    print(df.head())
    return {"message": "CSV subido correctamente", "rows": len(df)}



