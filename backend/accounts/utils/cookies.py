from django.conf import settings

from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .jwt import blacklist_refresh_token


# ============================================================
# INTERNAL COOKIE HELPER
# ============================================================

def _set_jwt_cookie(
    response: Response,
    token: str,
    *,
    token_type: str,
) -> Response:

    cookie_settings = settings.JWT_COOKIE

    if token_type == "access":

        cookie_name = cookie_settings["ACCESS_NAME"]
        cookie_path = cookie_settings["ACCESS_PATH"]

        max_age = int(
            settings.SIMPLE_JWT[
                "ACCESS_TOKEN_LIFETIME"
            ].total_seconds()
        )

    elif token_type == "refresh":

        cookie_name = cookie_settings["REFRESH_NAME"]
        cookie_path = cookie_settings["REFRESH_PATH"]

        max_age = int(
            settings.SIMPLE_JWT[
                "REFRESH_TOKEN_LIFETIME"
            ].total_seconds()
        )

    else:
        raise ValueError(
            "token_type must be 'access' or 'refresh'."
        )

    response.set_cookie(
        key=cookie_name,
        value=str(token),
        max_age=max_age,
        httponly=cookie_settings["HTTP_ONLY"],
        secure=cookie_settings["SECURE"],
        samesite=cookie_settings["SAMESITE"],
        path=cookie_path,
        domain=cookie_settings["DOMAIN"],
    )

    return response


# ============================================================
# PUBLIC HELPERS
# ============================================================

def set_access_cookie(
    response: Response,
    access_token: str,
) -> Response:

    return _set_jwt_cookie(
        response=response,
        token=access_token,
        token_type="access",
    )


def set_refresh_cookie(
    response: Response,
    refresh_token: str,
) -> Response:

    return _set_jwt_cookie(
        response=response,
        token=refresh_token,
        token_type="refresh",
    )


def set_jwt_cookies(
    response: Response,
    refresh: RefreshToken,
) -> Response:

    set_access_cookie(
        response,
        str(refresh.access_token),
    )

    set_refresh_cookie(
        response,
        str(refresh),
    )

    return response


# ============================================================
# CLEAR COOKIES
# ============================================================

def clear_jwt_cookies(
    response: Response,
) -> Response:

    cookie_settings = settings.JWT_COOKIE

    response.delete_cookie(
        key=cookie_settings["ACCESS_NAME"],
        path=cookie_settings["ACCESS_PATH"],
        domain=cookie_settings["DOMAIN"],
        samesite=cookie_settings["SAMESITE"],
    )

    response.delete_cookie(
        key=cookie_settings["REFRESH_NAME"],
        path=cookie_settings["REFRESH_PATH"],
        domain=cookie_settings["DOMAIN"],
        samesite=cookie_settings["SAMESITE"],
    )

    return response


# ============================================================
# COOKIE READERS
# ============================================================

def get_access_token(
    request: Request,
) -> str | None:

    return request.COOKIES.get(
        settings.JWT_COOKIE["ACCESS_NAME"]
    )


def get_refresh_token(
    request: Request,
) -> str | None:

    return request.COOKIES.get(
        settings.JWT_COOKIE["REFRESH_NAME"]
    )


# ============================================================
# LOGOUT HELPER
# ============================================================

def logout_user(
    request: Request,
    response: Response,
) -> Response:

    refresh_token = get_refresh_token(request)

    blacklist_refresh_token(refresh_token)

    clear_jwt_cookies(response)

    return response