from website import create_app
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from website.models import User
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str

class Login(BaseModel):
    email: str
    password: str

@app.post ("/users/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    from website.models import User
    user = User(email=user.email, first_name=user.first_name, password=pwd_context.hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return user






