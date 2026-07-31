from django.urls import path

from accounts.views.admin import (
    AdminUserListView,
    AdminUserDetailView,
    AdminUserUpdateView,
    DeactivateUserView,
    ReactivateUserView,
    DeleteUserView,
)

urlpatterns = [
    path(
        "users/",
        AdminUserListView.as_view(),
        name="admin-user-list",
    ),
    path(
        "users/<int:pk>/",
        AdminUserDetailView.as_view(),
        name="admin-user-detail",
    ),
    path(
        "users/<int:pk>/update/",
        AdminUserUpdateView.as_view(),
        name="admin-user-update",
    ),
    path(
        "users/<int:pk>/deactivate/",
        DeactivateUserView.as_view(),
        name="admin-user-deactivate",
    ),
    path(
        "users/<int:pk>/reactivate/",
        ReactivateUserView.as_view(),
        name="admin-user-reactivate",
    ),
    path(
        "users/<int:pk>/delete/",
        DeleteUserView.as_view(),
        name="admin-user-delete",
    ),
]