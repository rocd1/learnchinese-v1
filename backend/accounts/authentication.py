from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.utils.cookies import get_access_token


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        access_token = get_access_token(request)

        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)

        return (
            self.get_user(validated_token),
            validated_token,
        )