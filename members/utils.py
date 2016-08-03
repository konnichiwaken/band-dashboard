from authentication.models import Account
from members.models import BandMember
from members.models import Role


def initialize_roles():
    roles_to_initialize = ['Director', 'President', 'Secretary']
    for role in roles_to_initialize:
        try:
            Role.objects.get(name=role)
        except Role.DoesNotExist:
            Role.objects.create(name=role)


def initialize_test_accounts():
    test_accounts = [
        {
            'email': 'director@duke.edu',
            'first_name': 'Dir',
            'last_name': 'Ector',
            'role': 'Director',
            'password': 'director',
            'section': BandMember.DRUMLINE,
        },
        {
            'email': 'president@duke.edu',
            'first_name': 'Pres',
            'last_name': 'Ident',
            'role': 'President',
            'password': 'president',
            'section': BandMember.DRUMLINE,
        },
        {
            'email': 'secretary@duke.edu',
            'first_name': 'Sec',
            'last_name': 'Retary',
            'role': 'Secretary',
            'password': 'secretary',
            'section': BandMember.DRUMLINE,
        },
    ]
    for test_account in test_accounts:
        account_role = test_account.pop('role', None)
        password = test_account.pop('password')
        section = test_account.pop('section', None)
        account = Account(**test_account)
        account.set_password(password)
        account.save()
        if account_role:
            role = Role.objects.get(name=account_role)
            role.accounts.add(account)

        band_member = BandMember.objects.create(account=account, section=section)


def initialize():
    initialize_roles()
    initialize_test_accounts()
