from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()


# ============================================================
# REGISTER
# ============================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
        )

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():

            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password_confirm"]:

            raise serializers.ValidationError(
                {
                    "password_confirm":
                        "Passwords do not match."
                }
            )

        validate_password(attrs["password"])

        return attrs

    def create(self, validated_data):

        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user


# ============================================================
# LOGIN
# ============================================================


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:

            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:

            raise serializers.ValidationError(
                "This account has been disabled."
            )

        attrs["user"] = user

        return attrs


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(
                {
                    "confirm_password":
                        "Passwords do not match."
                }
            )

        validate_password(attrs["new_password"])

        return attrs

    def save(self, user):

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save(
            update_fields=["password"]
        )

        return user


# ============================================================
# FORGOT PASSWORD (Future)
# ============================================================

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


# ============================================================
# RESET PASSWORD (Future)
# ============================================================

class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(
                {
                    "confirm_password":
                        "Passwords do not match."
                }
            )

        validate_password(attrs["new_password"])

        return attrs


# ============================================================
# VERIFY EMAIL (Future)
# ============================================================

class VerifyEmailSerializer(serializers.Serializer):

    token = serializers.CharField()


# ============================================================
# RESEND VERIFICATION EMAIL (Future)
# ============================================================

class ResendVerificationSerializer(serializers.Serializer):

    email = serializers.EmailField()