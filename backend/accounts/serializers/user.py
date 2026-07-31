from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


# ============================================================
# USER PROFILE
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "username",
            "created_at",
            "updated_at",
        )


# ============================================================
# UPDATE PROFILE
# ============================================================

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "avatar",
        )

    def validate_email(self, value):

        value = value.lower()

        user = self.instance

        if (
            User.objects
            .exclude(pk=user.pk)
            .filter(email=value)
            .exists()
        ):

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value


# ============================================================
# UPDATE AVATAR
# ============================================================

class AvatarSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "avatar",
        )



# ============================================================
# DELETE ACCOUNT
# ============================================================

class DeleteAccountSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    confirmation = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )


    def validate_password(self, value):

        user = self.context["request"].user

        if not user.check_password(value):

            raise serializers.ValidationError(
                "Incorrect password."
            )

        return value


    def validate_confirmation(self, value):

        if value != "DELETE":

            raise serializers.ValidationError(
                "Please type DELETE to confirm."
            )

        return value