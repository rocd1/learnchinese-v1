from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


# ============================================================
# JWT HELPERS
# ============================================================

def create_tokens_for_user(user) -> RefreshToken:
    """
    Create JWT tokens for a user.
    """

    return RefreshToken.for_user(user)


def blacklist_refresh_token(
    refresh_token: str | None,
) -> bool:
    """
    Blacklist a refresh token.

    Returns:
        True if successful.
        False if missing or invalid.
    """

    if not refresh_token:
        return False

    try:
        RefreshToken(refresh_token).blacklist()
        return True

    except TokenError:
        return False


# ============================================================
# PASSWORD RESET TOKEN
# ============================================================

password_reset_token = PasswordResetTokenGenerator()


# ============================================================
# EMAIL VERIFICATION TOKEN
# ============================================================

email_verification_token = PasswordResetTokenGenerator()