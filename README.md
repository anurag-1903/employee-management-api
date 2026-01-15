# Employee Management API

A FastAPI-based backend application for managing employees with secure JWT authentication.

## 🚀 Features
- JWT-based Authentication
- Employee CRUD Operations
- Pagination & Search
- SQLAlchemy ORM
- SQLite Database
- Swagger API Documentation

## 🛠 Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)

## ⚙️ Setup Instructions

```bash
git clone <your-repo-url>
cd employee_api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app