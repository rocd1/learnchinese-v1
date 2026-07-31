```
django-secure-starter/
│
├── backend/
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── accounts/
│   │   ├── authentication.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   │
│   │   ├── serializers/
│   │   ├── views/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── frontend/
```


```
accounts/
│
├── migrations/
│
├── serializers/
│   ├── __init__.py
│   ├── auth.py
│   └── user.py
│
├── views/
│   ├── __init__.py
│   ├── auth.py
│   └── user.py
│
├── utils/
│   ├── __init__.py
│   ├── jwt.py
│   ├── cookies.py
│   └── tokens.py
│
├── services/
│   ├── __init__.py
│   ├── email.py
│   └── auth.py
│
├── admin.py
├── apps.py
├── authentication.py
├── models.py
├── permissions.py
├── signals.py
├── urls.py
├── tests.py
└── validators.py
```



======================UPDATED PROJECT ARCHITECTURE==========================
```
accounts/
│
├── migrations/
│
├── serializers/
│   ├── __init__.py
│   ├── authentication.py      # RegisterSerializer, LoginSerializer, etc.
│   └── user.py                # UserSerializer, UserUpdateSerializer
│
├── services/
│   ├── __init__.py
│   ├── authentication.py      # Register user, login workflow, etc.
│   └── email.py               # Email-related business logic
│
├── tests/
│   ├── __init__.py
│   ├── test_authentication.py
│   ├── test_models.py
│   ├── test_permissions.py
│   ├── test_serializers.py
│   ├── test_services.py
│   ├── test_utils.py
│   └── test_views.py
│
├── utils/
│   ├── __init__.py
│   ├── cookies.py             # Set/Clear HttpOnly cookies
│   ├── jwt.py                 # JWT helper functions
│   └── tokens.py              # Email verification/reset tokens
│
├── views/
│   ├── __init__.py
│   ├── authentication.py      # RegisterView, LoginView, LogoutView...
│   └── user.py                # MeView, UpdateProfileView
│
├── __init__.py
├── admin.py
├── apps.py
├── authentication.py          # Custom DRF authentication classes
├── models.py                  # User model
├── permissions.py             # Custom DRF permissions
├── signals.py
├── urls.py
└── validators.py

```

=======================================================

BUILD ORDER:


create project folder
create folder named backend
create README.md
open backend folder in integrated terminal
create venv
python -m venv venv
venv\Scripts\activate 
.vscode/settings.json

{
    "python.defaultInterpreterPath": "E:/django-secure-starter/backend/venv/Scripts/python.exe",
    "python.terminal.useEnvFile": true
}


pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-csp pillow 

django-admin startproject config .        

create folder backend/serializers
create folder backend/views
create folder backend/utils

backend/.env
backend/.gitignore

installed apps[
    'accounts',
]

runserver

settings.py
AUTH_USER_MODEL = "accounts.User"

models.py
```
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username
```

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

python manage.py createsuperuser
```
backends
aivasmm101@
backends1234567

roc
motivationfocus101
superroc
```

runserver

```

System check identified no issues (0 silenced).
July 27, 2026 - 20:23:24
Django version 6.0.7, using settings 'config.settings'
Starting development server at `http://127.0.0.1:8000/`
Quit the server with CTRL-BREAK.
```


configure `settings.py`
```
AUTH_USER_MODEL = "accounts.User"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```



register the user admin
```
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = (
        "username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "avatar",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
```

create utility files `utils.py`
```
accounts/

utils/
    __init__.py
    cookies.py
    jwt.py
    tokens.py
```
```
accounts/

utils/

    cookies.py
        _set_jwt_cookie()
        set_access_cookie()
        set_refresh_cookie()
        set_jwt_cookies()
        clear_jwt_cookies()
        get_access_token()
        get_refresh_token()
        logout_user()

    jwt.py
        create_tokens_for_user()
        blacklist_refresh_token()

    tokens.py
        email verification
        password reset
```
auth flow architecture
```
Login Request
      │
      ▼
Serializer
      │
      ▼
Authentication Service
      │
      ▼
JWT Utility
      │
      ▼
Cookie Utility
      │
      ▼
Response
```

==========================================================

create empty files and folders

create `accounts/authentication.py`

create `accounts/permissions.py`

create services
```
services/

authentication.py
email.py
```

create serializers
```
serializers/
authentication.py
user.py
```

create views
```
views/

authentication.py
user.py
```


configure settings.py
pip freeze > requirements.txt
pip install -r requirements.txt

```
# Django
Django==6.0.7
asgiref==3.12.1
sqlparse==0.5.5
tzdata==2026.3

# Django REST Framework
djangorestframework==3.17.1
djangorestframework_simplejwt==5.5.1
PyJWT==2.13.0

# Configuration & Security
django-environ==0.14.0
django-cors-headers==4.9.0
django-csp==4.0
whitenoise==6.12.0

# Images
Pillow==12.3.0

# Database (optional for PostgreSQL)
psycopg[binary]==3.2.10
```


build order
```models
    ↓
utils
    ↓
settings
    ↓
serializers
    ↓
authentication.py
    ↓
services
    ↓
views
    ↓
urls
    ↓
tests

```



=================================

authentication flow
```
POST /register/

        |
        v

Create User


POST /login/

        |
        v

Create RefreshToken

        |
        v

Set HTTP-only cookies


POST /logout/

        |
        v

Blacklist refresh token

        |
        v

Delete cookies

```



serializers folder
```
accounts/
│
└── serializers/
    │
    ├── __init__.py
    │
    ├── authentication.py
    │   ✅ RegisterSerializer
    │   ✅ LoginSerializer
    │   ✅ ChangePasswordSerializer
    │   ⚠ Forgot/Reset placeholders
    │
    ├── user.py
    │   ✅ UserProfileSerializer
    │   ✅ UserUpdateSerializer
    │   ✅ AvatarSerializer
    │   ✅ DeleteAccountSerializer
    │
    └── admin.py
        ✅ AdminUserListSerializer
        ✅ AdminUserDetailSerializer
        ✅ AdminUserUpdateSerializer
```


```
Authentication

✓ Register
✓ Login
✓ Logout
✓ Refresh Token
✓ Change Password
✓ Forgot Password
✓ Reset Password
✓ Verify Email
✓ Resend Verification Email
```


Then we create:

accounts/views/user.py

for:

Update Profile
Update Avatar
Delete Account

Then:

accounts/views/admin.py

for:

List Users
View User
Update User
Deactivate User
Reactivate User
Delete User


note: Future improvement: If you later decide to use soft deletes (is_active=False or a deleted_at field), you'll only change the section that calls user.delete().



urls
```
accounts/
│
├── urls/
│   ├── __init__.py
│   ├── authentication.py
│   ├── user.py
│   └── admin.py
│
└── urls.py
```


urls/authentication.py
```
Contains only authentication endpoints.

/api/auth/register/
/api/auth/login/
/api/auth/logout/
/api/auth/me/
/api/auth/change-password/
/api/auth/refresh/
/api/auth/forgot-password/
/api/auth/reset-password/
/api/auth/verify-email/
/api/auth/resend-verification/
```


urls/user.py
```
Contains endpoints for the currently logged-in user.

/api/user/profile/
/api/user/avatar/
/api/user/delete/
urls/admin.py

Contains administrator endpoints.

/api/admin/users/
/api/admin/users/<int:pk>/
/api/admin/users/<int:pk>/update/
/api/admin/users/<int:pk>/deactivate/
/api/admin/users/<int:pk>/reactivate/
/api/admin/users/<int:pk>/delete/
```


============

urls.py

This becomes the entry point for the app.
```
from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include("accounts.urls.authentication"),
    ),
    path(
        "user/",
        include("accounts.urls.user"),
    ),
    path(
        "admin/",
        include("accounts.urls.admin"),
    ),
]
```
Then in your project-level config/urls.py:
```
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/",
        include("accounts.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
```


(venv) PS E:\django-secure-starter\backend> tree /F accounts     
Folder PATH listing for volume All Soft
Volume serial number is 1433-32BC
E:\DJANGO-SECURE-STARTER\BACKEND\ACCOUNTS
│   admin.py
│   apps.py
│   authentication.py
│   models.py
│   permissions.py
│   signals.py
│   tests.py
│   views.py
│   __init__.py
│   
├───migrations
│   │   0001_initial.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           0001_initial.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───serializers
│   │   admin.py
│   │   authentication.py
│   │   user.py
│   │   
│   └───__pycache__
├───tests
├───urls
│   │   admin.py
│   │   authentication.py
│   │   users.py
│   │   
│   └───__pycache__
├───utils
│   │   cookies.py
│   │   email.py
│   │   jwt.py
│   │   tokens.py
│   │   
│   └───__pycache__
├───views
│   │   admin.py
│   │   authentications.py
│   │   user.py
│   │   
│   └───__pycache__
└───__pycache__
        admin.cpython-314.pyc
        apps.cpython-314.pyc
        models.cpython-314.pyc
        __init__.cpython-314.pyc

