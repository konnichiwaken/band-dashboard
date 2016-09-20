import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import Account
from authentication.permissions import CanCreateAccount
from authentication.permissions import IsAccountAdminOrAccountOwner
from authentication.serializers import AccountSerializer
from attendance.models import Band
from emails.tasks import send_unsent_emails
from members.models import BandMember


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (
        IsAccountAdminOrAccountOwner,
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

    def partial_update(self, request, pk=None):
        data = json.loads(request.body)
        if 'password' in data and request.user.id != int(pk):
            return Response({
                'status': "Forbidden",
                'message': "Don't have permission to update password",
            }, status=status.HTTP_403_FORBIDDEN)


        return super(AccountViewSet, self).partial_update(request, pk=pk)


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
            for band in Band.objects.all():
                band.unassigned_members.add(band_member)
                band.save()

        return Response({}, status=status.HTTP_201_CREATED)


class CreatePasswordView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        email = request.user.email
        password = data.get('password')
        if not email or not password:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(email=email)
            account.is_registered = True
            account.set_password(password)
            account.save()
            update_session_auth_hash(request, account)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Account.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
