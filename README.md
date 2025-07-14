# Patient-Management-system
This is a FastAPI-based backend project for managing patient records, including user authentication and CRUD operations on patient data.

## Features
- Add, update, delete patient records
- User registration and login with password hashing
- Input validation using Pydantic schemas
- PostgreSQL database with SQLAlchemy ORM

## Installation
1. Clone the repo:
git clone https://github.com/AnvithaYalamanchili/Patient-Management-system.git

2. cd Patient-Management-system

## Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

## Install dependencies
pip install -r requirements.txt

## Usage 
Run the app with uvicorn main:app --reload

