from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

def get_token(request):
    # Get the Authorization header from the request
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    # Check if the Authorization header exists and starts with 'Token '
    if authorization_header and authorization_header.startswith('Token '):
        # Extract the token from the header
        token = authorization_header.split(' ')[1]
        return token


def get_user_from_bearer_token(request):
    # Get the Authorization header from the request
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    # Check if the Authorization header exists and starts with 'Token '
    if authorization_header and authorization_header.startswith('Token '):
        # Extract the token from the header
        bearer_token = authorization_header.split(' ')[1]

        # Get the user based on the token
        try:
            token = Token.objects.get(key=bearer_token)
            user = token.user
            return user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

    # If no Bearer token is found, return None
    return None

