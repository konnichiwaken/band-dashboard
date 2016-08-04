from django.conf import settings
from itsdangerous import URLSafeTimedSerializer

from authentication.settings import ACCOUNT_CREATION_ADMIN_ROLES


def is_account_creation_admin(account):
    roles = set(account.roles.values_list('name', flat=True))
    return bool(roles.intersection(ACCOUNT_CREATION_ADMIN_ROLES))


def send_registration_email(account):
    token = generate_confirmation_token(account.email)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=settings.SECURITY_PASSWORD_SALT,
            max_age=expiration)
    except:
        return False

    return email
