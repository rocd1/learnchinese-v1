from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.admin import (
    AdminUserListSerializer,
    AdminUserDetailSerializer,
    AdminUserUpdateSerializer,
)

User = get_user_model()



# ============================================================
# LIST USERS
# ============================================================

class AdminUserListView(ListAPIView):

    permission_classes = [
        IsAdminUser,
    ]

    serializer_class = AdminUserListSerializer

    queryset = User.objects.all().order_by(
        "username",
    )


# ============================================================
# USER DETAIL
# ============================================================

class AdminUserDetailView(RetrieveAPIView):

    permission_classes = [
        IsAdminUser,
    ]

    serializer_class = AdminUserDetailSerializer

    queryset = User.objects.all()


# ============================================================
# UPDATE USER
# ============================================================

class AdminUserUpdateView(UpdateAPIView):

    permission_classes = [
        IsAdminUser,
    ]

    serializer_class = AdminUserUpdateSerializer

    queryset = User.objects.all()



# ============================================================
# DEACTIVATE USER
# ============================================================

class DeactivateUserView(APIView):

    permission_classes = [
        IsAdminUser,
    ]


    def post(self, request, pk):

        user = get_object_or_404(
            User,
            pk=pk,
        )

        user.is_active = False

        user.save(
            update_fields=[
                "is_active",
            ]
        )

        return Response(
            {
                "message":
                    "User deactivated.",
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# REACTIVATE USER
# ============================================================

class ReactivateUserView(APIView):

    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request, pk):

        user = get_object_or_404(
            User,
            pk=pk,
        )

        user.is_active = True

        user.save(
            update_fields=[
                "is_active",
            ]
        )

        return Response(
            {
                "message":
                    "User reactivated.",
            },
            status=status.HTTP_200_OK,
        )



# ============================================================
# DELETE USER
# ============================================================

class DeleteUserView(APIView):

    permission_classes = [
        IsAdminUser,
    ]

    def delete(self, request, pk):

        user = get_object_or_404(
            User,
            pk=pk,
        )

        user.delete()

        return Response(
            {
                "message":
                    "User deleted.",
            },
            status=status.HTTP_200_OK,
        )


