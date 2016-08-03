from authentication.settings import ACCOUNT_CREATION_ADMIN_ROLES


def is_account_creation_admin(account):
    roles = set(account.roles.values_list('name', flat=True))
    return bool(roles.intersection(ACCOUNT_CREATION_ADMIN_ROLES))


def create_account(account):
    print account
