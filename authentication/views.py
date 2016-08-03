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
from authentication.utils import create_account


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
        for account in data['accounts']:
            create_account(account)

        return Response({}, status=status.HTTP_201_CREATED)
