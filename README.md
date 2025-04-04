# oaktree-exam-fastapi

# Oaktree Exam - FastAPI Backend

This is the backend API for the Oaktree Exam project, built with **FastAPI**. It provides authentication, API endpoints, and database management.

## Tech Stack

- **FastAPI** - High-performance web framework
- **SQLAlchemy** - ORM for database interactions
- **Pydantic** - Data validation and serialization
- **bcrypt & passlib** - Secure password hashing
- **Python-Jose** - JWT authentication
- **Uvicorn** - ASGI server for FastAPI

## Project Structure

for testing
run pytest

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JustineLuys/oaktree-exam-fastapi.git
   cd oaktree-exam-fastapi
   python -m venv env
   source env/bin/activate
   Windows: env\Scripts\activate
   To install dependencies:
   pip install -r requirements.txt
   To run the app:
   uvicorn main:app --reload
