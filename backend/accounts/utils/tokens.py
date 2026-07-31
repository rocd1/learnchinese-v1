from django.contrib.auth.tokens import PasswordResetTokenGenerator


# ============================================================
# PASSWORD RESET TOKEN
# ============================================================

password_reset_token = PasswordResetTokenGenerator()


# ============================================================
# EMAIL VERIFICATION TOKEN
# ============================================================

email_verification_token = PasswordResetTokenGenerator()