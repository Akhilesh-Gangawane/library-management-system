# Library Management System

A full-stack Library Management System built with **FastAPI** (Python) following the **MVC pattern**, featuring JWT authentication, Alembic migrations, and a clean Bootstrap UI.

## Features

### User Side
- Register & Login
- View, Search, and Filter books
- View book details
- Borrow and Return books
- View borrowing history
- View profile

### Admin Side
- Add, Update, Delete books
- Add authors and categories
- View all users
- View all borrowing records
- Manage book availability

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** SQLite
- **Auth:** JWT (JSON Web Tokens)
- **Architecture:** MVC Pattern

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Seed the database:**
   ```bash
   python seed.py
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Open in browser:**
   ```
   http://localhost:8000
   ```

## Default Credentials

| Role  | Email              | Password  |
|-------|--------------------|-----------|
| Admin | admin@college.edu  | admin@123 |
| User  | user@email.com     | user@123  |

## Project Structure

```
library-mgmt-sys/
├── app/
│   ├── models/          # Database models (M)
│   ├── views/           # Templates (V)
│   ├── controllers/     # Route handlers (C)
│   ├── schemas/         # Pydantic schemas
│   ├── helpers/         # Utility functions
│   ├── config.py        # App configuration
│   ├── database.py      # DB connection
│   └── main.py          # App entry point
├── alembic/             # Database migrations
├── static/              # CSS, JS assets
├── postman/             # Postman collection
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── seed.py              # Database seeder
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Postman Collection

Import the Postman collection from `postman/Library_Management_System.postman_collection.json` to test all API endpoints.
