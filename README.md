![Python](https://img.shields.io/badge/Python-3.14-blue)

![Django](https://img.shields.io/badge/Django-6.0-green)

![License](https://img.shields.io/badge/License-MIT-yellow)


# Django Secure Starter

A secure, production-ready Django REST Framework starter template featuring cookie-based JWT authentication, modern security defaults, environment-based configuration, and a clean project structure for building scalable APIs.

---

## Features

- Django 6
- Django REST Framework
- Cookie-based JWT Authentication
- Refresh Token Rotation
- Token Blacklisting
- Custom User Model
- Environment Variables using django-environ
- CORS Configuration
- Content Security Policy (CSP)
- WhiteNoise Static File Support
- Rotating Log Files
- PostgreSQL Ready
- SQLite Development Support
- Secure Production Defaults
- Modular Accounts App
- Organized Views, URLs, Serializers and Utilities

---

## Technology Stack

Backend

- Python 3.14+
- Django 6
- Django REST Framework
- Simple JWT

Security

- Cookie JWT Authentication
- CSP
- CORS
- Secure Cookies
- CSRF Protection

Deployment

- WhiteNoise
- Gunicorn
- PostgreSQL

---

## Project Structure

```
backend/

accounts/
    serializers/
    urls/
    utils/
    views/
    models.py
    authentication.py

config/
    settings.py
    urls.py

logs/
media/

requirements.txt
.env.example
```

```
django-secure-starter/
│
├── backend/
│   ├── accounts/
│   ├── config/
│   ├── media/
│   ├── logs/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│
├── README.md
├── LICENSE
└── .gitignore
```


---

## Installation

Clone the repository

```bash
git clone https://github.com/rocd1/django-secure-starter.git
```

Go into backend

```bash
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Copy the environment file

```bash
copy .env.example .env
```

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the server

```bash
python manage.py runserver
```

---

## Environment Variables

Example

```env
DEBUG=True

SECRET_KEY=change-me

DATABASE_URL=sqlite:///db.sqlite3

TIME_ZONE=Asia/Singapore

ALLOWED_HOSTS=127.0.0.1,localhost

CORS_ALLOWED_ORIGINS=http://localhost:4200

DEFAULT_FROM_EMAIL=noreply@example.com
```

---

## Included Authentication APIs

```
| Method | Endpoint                     | Description          |
| ------ | ---------------------------- | -------------------- |
| POST   | `/api/auth/register/`        | Register             |
| POST   | `/api/auth/login/`           | Login                |
| POST   | `/api/auth/logout/`          | Logout               |
| POST   | `/api/auth/refresh/`         | Refresh Access Token |
| POST   | `/api/auth/change-password/` | Change Password      |
| GET    | `/api/auth/me/`              | Current User         |
```


Authentication

- Register
- Login
- Logout
- Refresh Token
- Change Password
- User Profile

---

## Security

This starter includes

- HttpOnly JWT Cookies
- Refresh Token Rotation
- Token Blacklisting
- CSP Headers
- Secure Cookies
- CORS Configuration
- Environment Variable Configuration
- Rotating Logs
- WhiteNoise Static Files
- Password Validation

---

## Logging

Log files are automatically created in

```
backend/logs/
```

Files

- django.log
- security.log

---

## Production Ready

Supports

- PostgreSQL
- Gunicorn
- WhiteNoise
- Secure HTTPS Cookies
- HSTS
- CSP
- Environment Variables

---


##ROADMAP
```
## Roadmap

- [x] Cookie JWT Authentication
- [x] Custom User Model
- [x] Logging
- [x] Environment Variables
- [x] PostgreSQL Support
- [ ] Email Verification
- [ ] Password Reset
- [ ] Two-Factor Authentication
- [ ] Docker Support
- [ ] CI/CD Pipeline
```

```
README.md

├── Title
├── Badges
├── Description
├── Features
├── Technology Stack
├── Project Structure
├── Installation
├── Environment Variables
├── API Endpoints
├── Security Features
├── Logging
├── Production Deployment
├── Roadmap
├── License
```


## License

MIT License