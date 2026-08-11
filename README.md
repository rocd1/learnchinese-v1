![Python](https://img.shields.io/badge/Python-3.14-blue)

![Django](https://img.shields.io/badge/Django-6.0-green)

![License](https://img.shields.io/badge/License-MIT-yellow)


# Learn Mandarin Chinese

A secure free application for learning mandarin, featuring cookie-based JWT authentication, modern security defaults, environment-based configuration, and a clean structure APIs.

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
learnchinese-v1/
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



## License

MIT License