from django.conf import settings
from itsdangerous import URLSafeTimedSerializer

from authentication.settings import ACCOUNT_CREATION_ADMIN_ROLES
from emails.models import Email


def is_account_creation_admin(account):
    try:
        roles = set(account.roles.values_list('name', flat=True))
    except AttributeError:
        return False
    else:
        return bool(roles.intersection(ACCOUNT_CREATION_ADMIN_ROLES))
