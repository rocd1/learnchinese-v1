from rest_framework import status

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework.response import Response

from rest_framework.throttling import (
    ScopedRateThrottle,
)

from rest_framework.views import APIView


from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
)

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)


from accounts.serializers.authentication import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
    ResendVerificationSerializer,
)


from accounts.serializers.user import (
    UserProfileSerializer,
)


from accounts.utils.jwt import (
    create_tokens_for_user,
    blacklist_refresh_token,
)

from accounts.utils.cookies import (
    set_jwt_cookies,
    clear_jwt_cookies,
    get_refresh_token,
)



# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):
    """
    Register a new user.
    """

    permission_classes = [
        AllowAny,
    ]


    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )


        serializer.save()


        return Response(
            {
                "message":
                    "Registration successful.",
            },
            status=status.HTTP_201_CREATED,
        )



# ============================================================
# LOGIN
# ============================================================

class LoginView(APIView):
    """
    Authenticate user and create JWT cookies.
    """


    permission_classes = [
        AllowAny,
    ]


    throttle_classes = [
        ScopedRateThrottle,
    ]


    throttle_scope = "login"



    def post(self, request):

        serializer = LoginSerializer(
            data=request.data,
        )


        serializer.is_valid(
            raise_exception=True,
        )


        user = serializer.validated_data["user"]


        refresh = create_tokens_for_user(
            user,
        )


        response = Response(
            {
                "message":
                    "Login successful.",
            },
            status=status.HTTP_200_OK,
        )


        set_jwt_cookies(
            response,
            refresh,
        )


        return response


# ============================================================
# LOGOUT
# ============================================================

class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    def post(self, request):

        refresh_token = get_refresh_token(
            request,
        )


        blacklist_refresh_token(
            refresh_token,
        )


        response = Response(
            {
                "message":
                    "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )


        clear_jwt_cookies(
            response,
        )


        return response







# ============================================================
# CURRENT USER
# ============================================================

class MeView(APIView):
    """
    Return the authenticated user's profile.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        serializer = UserProfileSerializer(
            request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordView(APIView):
    """
    Change the authenticated user's password.

    After changing the password, the current
    refresh token is blacklisted and both
    JWT cookies are cleared.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    throttle_classes = [
        ScopedRateThrottle,
    ]

    throttle_scope = "password_reset"

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):

            return Response(
                {
                    "old_password": [
                        "Current password is incorrect."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(
            user,
        )

        refresh_token = get_refresh_token(
            request,
        )

        blacklist_refresh_token(
            refresh_token,
        )

        response = Response(
            {
                "message": (
                    "Password changed successfully. "
                    "Please log in again."
                )
            },
            status=status.HTTP_200_OK,
        )

        clear_jwt_cookies(
            response,
        )

        return response



# ============================================================
# REFRESH TOKEN
# ============================================================

class RefreshTokenView(APIView):
    """
    Refresh JWT tokens using the refresh token
    stored in the HTTP-only cookie.
    """

    authentication_classes = []

    permission_classes = [
        AllowAny,
    ]

    throttle_classes = [
        ScopedRateThrottle,
    ]

    throttle_scope = "refresh"

    def post(self, request):

        refresh = get_refresh_token(
            request,
        )

        if not refresh:

            return Response(
                {
                    "detail": "Refresh token not found."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(
            data={
                "refresh": refresh,
            }
        )

        serializer.is_valid(
            raise_exception=True,
        )


        new_refresh = RefreshToken(
            serializer.validated_data["refresh"]
        )

        response = Response(
            {
                "message": (
                    "Token refreshed successfully."
                )
            },
            status=status.HTTP_200_OK,
        )

        set_jwt_cookies(
            response,
            new_refresh,
        )

        return response




        '''
        refresh_token = RefreshToken(
            serializer.validated_data["refresh"]
        )

        response = Response(
            {
                "message": (
                    "Token refreshed successfully."
                )
            },
            status=status.HTTP_200_OK,
        )

        set_jwt_cookies(
            response,
            refresh_token,
        )

        return response
    '''







#placeholder views for future

# ============================================================
# FORGOT PASSWORD (Future)
# ============================================================

class ForgotPasswordView(APIView):

    permission_classes = [
        AllowAny,
    ]

    throttle_classes = [
        ScopedRateThrottle,
    ]

    throttle_scope = "password_reset"

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            {
                "message": (
                    "Password reset is not yet implemented."
                )
            },
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )



# ============================================================
# RESET PASSWORD (Future)
# ============================================================

class ResetPasswordView(APIView):

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            {
                "message": (
                    "Password reset is not yet implemented."
                )
            },
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )



# ============================================================
# VERIFY EMAIL (Future)
# ============================================================

class VerifyEmailView(APIView):

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        serializer = VerifyEmailSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            {
                "message": (
                    "Email verification is not yet implemented."
                )
            },
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )



# ============================================================
# RESEND VERIFICATION EMAIL (Future)
# ============================================================

class ResendVerificationView(APIView):

    permission_classes = [
        AllowAny,
    ]

    throttle_classes = [
        ScopedRateThrottle,
    ]

    throttle_scope = "signup"

    def post(self, request):

        serializer = ResendVerificationSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            {
                "message": (
                    "Email verification is not yet implemented."
                )
            },
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )    