from rest_framework import authentication
from rest_framework import exceptions
from .models import AuthToken

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return None  # No token provided

        try:
            auth_token = AuthToken.objects.get(token=token)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (auth_token.user, None)
