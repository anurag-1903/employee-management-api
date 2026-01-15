from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.database import engine
from app import models
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.routes import employees

app = FastAPI(
    title="Employee Management API",
    description="CRUD API with JWT Authentication",
    version="1.0.0"
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# 🔐 TOKEN ENDPOINT (THIS WAS MISSING)
@app.post("/api/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Employee routes
app.include_router(employees.router)