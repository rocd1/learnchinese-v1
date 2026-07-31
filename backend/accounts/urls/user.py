from django.urls import path

from accounts.views.user import (
    UpdateProfileView,
    UpdateAvatarView,
    DeleteAccountView,
)

urlpatterns = [
    path(
        "profile/",
        UpdateProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "avatar/",
        UpdateAvatarView.as_view(),
        name="update-avatar",
    ),
    path(
        "delete/",
        DeleteAccountView.as_view(),
        name="delete-account",
    ),
]