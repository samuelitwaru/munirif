# middleware.py
from datetime import timedelta
from django.utils import timezone
import threading
from accounts.utils import get_token, get_user_from_bearer_token
from rest_framework.authtoken.models import Token


_request_local = threading.local()

def get_current_request():
    return getattr(_request_local, 'request', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/api/accounts/refresh-token/'):
            return self.get_response(request)

        key = get_token(request)
        token = Token.objects.filter(key=key).first()
        if token:
            expiration_time = token.created + timedelta(hours=24)
            if timezone.now() > expiration_time:
                token.delete()
                
        # if token and token.created
        _request_local.request = request
        response = self.get_response(request)
        return response
    