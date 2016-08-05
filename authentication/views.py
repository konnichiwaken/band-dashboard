import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import Account
from authentication.permissions import CanCreateAccount
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from authentication.utils import confirm_token
from authentication.utils import send_registration_email
from emails.utils import send_unsent_emails
from members.models import BandMember


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (
        CanCreateAccount,
        IsAccountOwner,
        IsAuthenticated,
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.',
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Email/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CreateAccountsView(views.APIView):
    permission_classes = (CanCreateAccount, IsAuthenticated,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        for account_data in data['accounts']:
            section = account_data.pop('section')
            account = Account.objects.create_user(**account_data)
            band_member = BandMember.objects.create(section=section, account=account)
            send_registration_email(account)

        send_unsent_emails()
        return Response({}, status=status.HTTP_201_CREATED)


class ConfirmAccountView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        token = data.get('token')
        if token:
            email = confirm_token(token)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'email': email,
                    'name': account.get_full_name(),
                }, status=status.HTTP_200_OK)


class CreatePasswordView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(email=email)
            account.is_active = True
            account.set_password(password)
            account.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Account.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
