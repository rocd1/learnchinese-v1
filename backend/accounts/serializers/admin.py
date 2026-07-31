from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


# ============================================================
# ADMIN USER LIST
# ============================================================

class AdminUserListSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "created_at",
        )

        read_only_fields = fields




# ============================================================
# ADMIN USER DETAIL
# ============================================================

class AdminUserDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
        )



# ============================================================
# ADMIN UPDATE USER
# ============================================================

class AdminUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "is_active",
            "is_staff",
        )