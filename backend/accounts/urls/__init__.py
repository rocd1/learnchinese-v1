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