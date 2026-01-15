from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: Optional[str]
    role: Optional[str]
    date_joined: date

    class Config:
        orm_mode = True