CHECKLIST

```
accounts/

models.py                    ✅ Done

utils/
    jwt.py                   ✅ Done
    cookies.py               ✅ Done
    tokens.py                ✅ Done

settings.py                  ✅ Done

serializers/
    __init__.py
    auth.py
    user.py                  ← Next

authentication.py

permissions.py

services/
    auth.py
    email.py

views/
    auth.py
    user.py

urls.py

admin.py

signals.py

validators.py

tests/
```




```
django-secure-starter/
│
├── README.md              ✅ Main project documentation
├── LICENSE                ✅ Project license
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .gitignore
│   ├── .env.example
│   ├── notes.md           (optional)
│   ├── build_order.md     (optional)
│   │
│   ├── config/
│   ├── accounts/
│   ├── media/
│   ├── logs/
│   └── ...
│
└── frontend/
```


shell command
```
mkdir api-tests; cd api-tests; ni .env, auth.http, hsk.http, vocabulary.http, favorites.http, learning.http, quiz.http
```


```
# REST Client private environment
api-tests/.env


backend/
├── .env
│
├── api-tests/
│
│   ├── auth.http
│   ├── hsk.http
│   ├── vocabulary.http
│   ├── favorites.http
│   ├── learning.http
│   └── quiz.http
│
├── accounts/
├── learning/
├── config/
└── manage.py
```