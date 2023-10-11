from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from accounts.filters import UserFilter
from accounts.forms import CompleteSignupForm

from accounts.utils import get_user_from_bearer_token
from core.models import Profile
from utils.mails import send_html_email
from .serializers import CompleteSignupSerializer, GroupSerializer, PasswordChangeSerializer, PasswordResetSerializer, SetPasswordSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    filter_backends = [UserFilter]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.groups.add(Group.objects.get(name='applicant'))
            profile = Profile(
                user=user,
                faculty_id=request.data['faculty'],
                department_id=request.data['department'],
                qualification_id=request.data['qualification'],
                phone=request.data['phone'],
                gender=request.data['gender'],
                )
            profile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteSignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CompleteSignupSerializer(data=request.data)
        if serializer.is_valid():
            token = Token.objects.get(key=request.data['token'])
            user = token.user
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.email = user.username
            user.is_active = True
            user.set_password(request.data['password'])
            user.save()
            user.groups.add(Group.objects.get(name='reviewer'))
            profile = Profile(
                user=user,
                faculty_id=request.data['faculty'],
                department_id=request.data['department'],
                qualification_id=request.data['qualification'],
                phone=request.data['phone'],
                gender=request.data['gender'],
                )

            profile.save()
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLoginView(ObtainAuthToken):

    permission_classes = (AllowAny,)
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        groups = [group.name for group in user.groups.all()]
        token, created = Token.objects.get_or_create(user=user)
        res = {
            'token': token.key,
            'user': {
                'user_id': user.pk,
                'name': f'{user.first_name} {user.last_name}',
                'email': user.email,
                'groups': groups
            }
        }
        return Response(res)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        print(username, password)

        if user:
            login(request, user)
            user_data = UserSerializer(user).data
            user_data['groups'] = [group.name for group in user.groups.all()]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user_data})
        else:
            return Response({'error': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if request.META.get('HTTP_AUTHORIZATION'):
            _, key = request.META.get('HTTP_AUTHORIZATION').split(' ')
            token = Token.objects.filter(key=key).first()
            if token: token.delete()
        
        return Response({}, status=status.HTTP_200_OK)
    

class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = get_user_from_bearer_token(request)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Change the password and update session authentication hash
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep the user authenticated

        return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        # set token
        data = serializer.data
        user = User.objects.filter(username=data.get('email')).first()
        token, created = Token.objects.get_or_create(user=user)
        # send email token
        context = {
            'user': user, 'token':token, 'client_address': settings.CLIENT_ADDRESS
            }
        send_html_email(
            request,
            'PASSWORD RESET',
            [user.username],
            'emails/password-reset.html',
            context
            )

        return Response({'detail': 'A link has been sent to your email. Click the link to reset your password'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def set_password(request):
    serializer = SetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        # set token
        data = serializer.data
        token = Token.objects.get(key=data['token'])
        if token:
            user = token.user
            print(user)
            print(data['new_password'])
            user.set_password(data['new_password'])
            user.save()
            return Response({'detail': 'Your password has been updated'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def complete_signup(request):
    token = Token.objects.filter(key=token).first()
    _next = request.GET.get("next")
    complete_signup_form = CompleteSignupSerializer()

    if token:
        user = token.user
        if request.method == 'POST':
            complete_signup_form = CompleteSignupForm(request.POST)
            if complete_signup_form.is_valid():
                data = complete_signup_form.cleaned_data
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.set_password(data['password'])
                user.save()

                user.groups.add(Group.objects.get(name='reviewer'))
                
                context = {
                    'new_window_url': _next
                }
                return render(request, 'blank.html', context)
    else:
        messages.error(request, 'Invalid Request', extra_tags='danger')
    context = {
        'complete_signup_form': complete_signup_form,
        'token': token
    }
    return render(request, 'account/complete-signup.html', context)

def complete_signup2(request):
    token = request.GET.get("token")
    token = Token.objects.filter(key=token).first()
    _next = request.GET.get("next")
    complete_signup_form = CompleteSignupForm()

    if token:
        user = token.user
        if request.method == 'POST':
            complete_signup_form = CompleteSignupForm(request.POST)
            if complete_signup_form.is_valid():
                data = complete_signup_form.cleaned_data
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.set_password(data['password'])
                user.save()

                user.groups.add(Group.objects.get(name='reviewer'))
                
                context = {
                    'new_window_url': _next
                }
                return render(request, 'blank.html', context)
    else:
        messages.error(request, 'Invalid Request', extra_tags='danger')
    context = {
        'complete_signup_form': complete_signup_form,
        'token': token
    }
    return render(request, 'account/complete-signup.html', context)