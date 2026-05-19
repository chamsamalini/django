# py-django

This project is a beginner-friendly personal banking MVP built with Django, SQLite, server-rendered templates, pytest, and Waitress.

## Features

- Register a bank account
- View account details and current balance
- Deposit money
- Withdraw money without allowing overdrafts
- View transaction history newest first

## Local Setup

1. Create and activate the virtual environment.
2. Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Set environment variables or load them from your shell:

```powershell
$env:DJANGO_SECRET_KEY="replace-with-local-secret-key"
$env:DJANGO_DEBUG="True"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
```

4. Run migrations:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

5. Start the development server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

## Running Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

This command also generates `coverage.xml` for Sonar analysis.

## Windows Deployment With Waitress

Use Waitress for simple local Windows hosting:

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=0.0.0.0:8000 banking_project.wsgi:application
```
