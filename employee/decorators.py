from django.http import JsonResponse
from functools import wraps
from blog.models import AuthToken
from rest_framework import status

def token_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Authorization token required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Support for "Bearer <token>" format
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        try:
            auth_token = AuthToken.objects.get(token=token)
            request.user = auth_token.user
        except AuthToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = getattr(request, 'user', None)
            if user is None:
                return JsonResponse({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.role not in allowed_roles:
                return JsonResponse({'error': 'You don\'t have permissions'}, status=status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
