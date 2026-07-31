# Django Secure Starter

> A reusable, production-ready Django REST Framework starter template with secure authentication, best practices, and a clean architecture.

---

# Goal

This project is **not an application**.

It is a **starter template** that can be copied and reused whenever building a new Django REST API.

After completing this project you should have:

- ✅ Secure Django project structure
- ✅ Custom User model
- ✅ JWT Authentication using HttpOnly Cookies
- ✅ Role-based permissions
- ✅ Production-ready settings
- ✅ Logging
- ✅ Security middleware
- ✅ Email support
- ✅ Reusable utilities
- ✅ Clean folder structure
- ✅ Ready to connect to any frontend (Angular, React, Vue, Mobile)

---

# Technology Stack

- Python 3.13+
- Django 5+
- Django REST Framework
- SimpleJWT
- PostgreSQL
- django-environ
- django-cors-headers
- django-csp
- Pillow

---

# Project Structure

```
django-secure-starter/

backend/
│
├── config/
├── accounts/
├── manage.py
├── requirements.txt
├── .env.example
└── README.md

frontend/
```

---

# Development Roadmap

Build the project in the following order.

---

# Phase 1 — Project Setup

## Objectives

Create the Django project and install dependencies.

### Tasks

- Create virtual environment
- Install requirements
- Create Django project
- Create accounts app
- Configure settings.py
- Configure .env
- Connect PostgreSQL
- Run initial migrations
- Create superuser
- Verify Admin works

**Checkpoint**

You should now have:

- Working Django server
- PostgreSQL connected
- Admin login working

---

# Phase 2 — Clean Project Structure

## Objectives

Organize the project before adding features.

### Create folders

```
accounts/

├── migrations/

├── serializers/

├── views/

├── services/

├── utils/

├── tests/

├── templates/

├── management/

│   └── commands/

├── admin.py

├── apps.py

├── models.py

├── permissions.py

├── authentication.py

├── signals.py

├── urls.py
```

Also inside config create:

```
config/

settings.py

urls.py

wsgi.py

asgi.py
```

---

## Configure

- MEDIA_ROOT
- MEDIA_URL
- STATIC_ROOT
- STATIC_URL

---

# Phase 3 — Environment Configuration

## Objectives

Move every secret into environment variables.

Configure:

- SECRET_KEY
- DEBUG
- DATABASE_URL
- ALLOWED_HOSTS
- CORS_ALLOWED_ORIGINS
- EMAIL settings
- JWT settings

Create:

```
.env.example
```

Never commit:

```
.env
```

---

# Phase 4 — Custom User Model

## Objectives

Replace Django's default User model before creating migrations.

Create:

```
User(AbstractUser)
```

Suggested fields:

- avatar
- email
- created_at
- updated_at

Configure

```
AUTH_USER_MODEL
```

Run migrations.

**Checkpoint**

Admin login still works.

---

# Phase 5 — Authentication

## Objectives

Implement secure authentication.

Features:

- Register
- Login
- Logout
- Refresh Token
- Current User

Authentication should use:

- JWT
- HttpOnly Cookies
- Refresh Token Rotation
- Token Blacklisting

Do NOT store JWT inside localStorage.

---

# Phase 6 — Cookie Helpers

Create reusable helper functions.

Suggested utilities:

```
utils/

jwt.py
```

Functions:

- set_access_cookie()
- set_refresh_cookie()
- clear_auth_cookies()
- create_tokens_for_user()
- blacklist_refresh_token()

These helpers should be reusable in every future project.

---

# Phase 7 — Authentication Classes

Create

```
authentication.py
```

Build

```
CookieJWTAuthentication
```

The authentication class should read the access token from cookies instead of Authorization headers.

---

# Phase 8 — Serializers

Split serializers into separate files.

Example

```
serializers/

auth.py

user.py
```

Authentication serializers:

- RegisterSerializer
- LoginSerializer
- ChangePasswordSerializer

User serializers:

- UserSerializer
- UserUpdateSerializer

---

# Phase 9 — Views

Split views into modules.

```
views/

auth.py

user.py
```

Authentication Views

- Register
- Login
- Logout
- Refresh
- Me

User Views

- Profile
- Update Profile

---

# Phase 10 — URLs

Keep urls.py clean.

Example

```
accounts/

urls.py
```

Include inside config.

---

# Phase 11 — Permissions

Create

```
permissions.py
```

Build reusable permissions.

Examples

- IsOwner
- IsAdmin
- IsStaff
- ReadOnly
- IsAdminOrReadOnly

---

# Phase 12 — Groups & Roles

Create management command.

```
python manage.py create_roles
```

Automatically create:

- Admin
- Staff
- User

Assign permissions automatically.

This makes every new project consistent.

---

# Phase 13 — Admin Panel

Customize Django Admin.

Improve:

- User list
- Search
- Filters
- Ordering
- Readonly fields

Make Admin useful.

---

# Phase 14 — Logging

Create logs folder.

Configure logging.

Files:

```
logs/

django.log

security.log
```

Log:

- Login attempts
- Permission denied
- Errors
- Warnings

---

# Phase 15 — Security Hardening

Configure:

- CSP
- CORS
- CSRF
- Secure Cookies
- XSS Protection
- Clickjacking Protection
- HSTS
- SSL Redirect (Production)

---

# Phase 16 — Email

Configure SMTP.

Create reusable email service.

Example

```
services/email.py
```

Future projects can reuse this.

---

# Phase 17 — Signals

Create

```
signals.py
```

Examples

- Create profile
- Log login
- Log logout

---

# Phase 18 — Utilities

Create reusable helper functions.

Example

```
utils/

files.py

validators.py

responses.py

pagination.py

permissions.py

dates.py
```

These should be generic.

---

# Phase 19 — Global API Responses

Create a consistent response format.

Example

Success

```json
{
    "success": true,
    "message": "Login successful",
    "data": {}
}
```

Error

```json
{
    "success": false,
    "message": "Validation failed",
    "errors": {}
}
```

---

# Phase 20 — Testing

Create tests for

- Authentication
- Permissions
- Registration
- Login
- Logout
- JWT Refresh

Aim for high coverage before using this starter in other projects.

---

# Phase 21 — Production Checklist

Before using this starter in another project:

- DEBUG=False
- Secure Cookies enabled
- HTTPS
- HSTS
- CSP configured
- Strong SECRET_KEY
- Environment variables configured
- Static files collected
- Logging enabled
- Backup strategy planned

---

# Recommended Build Order

```
1. Project Setup
2. Folder Structure
3. Environment Variables
4. Custom User
5. Authentication
6. JWT Cookies
7. Authentication Class
8. Serializers
9. Views
10. URLs
11. Permissions
12. Roles
13. Admin
14. Logging
15. Security
16. Email
17. Signals
18. Utilities
19. API Responses
20. Tests
21. Production Review
```

---

# Future Features (Optional)

This starter intentionally excludes application-specific features.

Possible additions for future projects:

- Social Login
- Google OAuth
- GitHub OAuth
- Password Reset
- Email Verification
- Two-Factor Authentication (2FA)
- API Rate Limiting
- User Activity Logs
- Audit Trails
- Notifications
- Celery + Redis
- Background Tasks
- File Upload Service
- Object Storage (AWS S3 / Cloudflare R2)
- Docker Support
- CI/CD Pipeline
- Health Check Endpoint
- OpenAPI / Swagger Documentation

---

# Project Philosophy

This starter is designed around three principles:

- **Security First** — Secure defaults should come before convenience.
- **Reusable Architecture** — Keep code generic so it can be copied into any future Django project.
- **Beginner Friendly** — Build features in small, understandable steps instead of relying on "magic" or overly complex abstractions.

By the end of this project, you'll have a secure, maintainable foundation that can be reused for APIs such as learning platforms, e-commerce sites, booking systems, dashboards, and other Django REST applications.



















