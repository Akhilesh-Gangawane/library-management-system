# Library Management System

A full-stack Library Management System built with **FastAPI** (Python) following the **MVC pattern**, featuring JWT authentication, Alembic migrations, SQLAlchemy ORM (with SQLite and MySQL support), and a clean Bootstrap UI.

## Features

### User Side
- Register & Login with JWT authentication
- View, Search, and Filter books (search across titles, ISBN, publisher, authors, and categories)
- View book details with real-time copy availability
- Borrow and Return books with automatic stock management
- View personal borrowing history
- View and update user profile

### Admin Side
- Add, Update, and Delete books
- Add authors and categories
- View all registered users
- View and filter all borrowing records across all users
- Manage book availability and stock copies

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy (ORM), Alembic, PyMySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** SQLite (default local) / MySQL (production ready)
- **Auth:** JWT (JSON Web Tokens) with bcrypt password hashing
- **Architecture:** Strict MVC Pattern (Model-View-Controller)
- **API Testing:** Postman Collection & Automated E2E Test Suite

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vivek-Ghanwat/library-management-system.git
   cd library-management-system
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   Copy the example `.env` file:
   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env
   # Linux / Mac
   cp .env.example .env
   ```
   *By default, `DATABASE_URL` is configured for SQLite (`sqlite:///./library.db`).*
   *To use MySQL, update `DATABASE_URL` in `.env`:*
   ```env
   DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:3306/<dbname>?charset=utf8mb4
   ```

6. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

7. **Seed the database:**
   ```bash
   python seed.py
   ```

8. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

9. **Open in browser:**
   ```
   http://localhost:8000
   ```

## Default Credentials

| Role  | Email              | Password  |
|-------|--------------------|-----------|
| Admin | admin@college.edu  | admin@123 |
| User  | user@email.com     | user@123  |

## Running Tests

Run the complete end-to-end system test suite (covers all HTML routes, authentication, joins, borrowing lifecycle, and admin role permissions):
```bash
python test_system.py
```

## Project Structure

```
library-mgmt-sys/
├── app/
│   ├── models/          # SQLAlchemy ORM Database models (M)
│   ├── views/           # Route endpoints & Jinja2 templates (V)
│   ├── controllers/     # Business logic & operations (C)
│   ├── schemas/         # Pydantic schemas
│   ├── helpers/         # Utility functions (auth, response, validation)
│   ├── middlewares/     # JWT authentication middleware
│   ├── config.py        # App configuration & environment loader
│   ├── database.py      # Universal DB engine (SQLite / MySQL)
│   └── main.py          # App entry point
├── alembic/             # Database migrations
├── static/              # CSS, JS assets
├── postman/             # Postman collection with automated test scripts
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── seed.py              # Database seeder
└── test_system.py       # End-to-end automated test suite
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Postman Collection

Import the Postman collection from `postman/Library_Management_System.postman_collection.json` into Postman to test all API endpoints:
1. Set the variable `{{baseUrl}}` to `http://localhost:8000`.
2. Run **Login User** or **Login Admin** under `1. Authentication` — JWT tokens are automatically captured and assigned to subsequent requests via Postman test scripts.
