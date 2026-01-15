from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)

@router.post("/", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get("/", response_model=List[schemas.EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    query = db.query(models.Employee)

    if search:
        query = query.filter(models.Employee.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    data: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()