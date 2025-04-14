from django.shortcuts import render, get_object_or_404
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
from rest_framework.decorators import action
from accounts.utils import get_user_from_bearer_token
from core.models import Profile, ProfileTheme, Theme
from utils.mails import send_html_email
from .serializers import CompleteSignupSerializer, GroupSerializer, PasswordChangeSerializer, PasswordResetSerializer, SetPasswordSerializer, UpdateUserSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from templated_email import send_templated_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [UserFilter]

    @action(detail=False, methods=['GET'], name='get_user_by_token', url_path=r'get-user-by-token/(?P<token>[^/.]+)')
    def get_user_by_token(self, request, token, *args, **kwargs):
        token = get_object_or_404(Token, key=token)
        user = token.user
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['POST'], name='create_reviewer', url_path=r'create-reviewer')
    def create_reviewer(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.groups.add(Group.objects.get(name='reviewer'))
            profile = user.profile
            profile.user=user
            profile.faculty_id=request.data['faculty']
            profile.department_id=request.data['department']
            profile.qualification_id=request.data['qualification']
            profile.phone=request.data['phone']
            profile.gender=request.data['gender']
            profile.designation=request.data['designation']
            profile.save()
            theme_ids = request.data.get('themes')
            
            for theme_id in theme_ids:
                ProfileTheme.objects.create(theme_id=theme_id, profile=profile)
            
            token, created = Token.objects.get_or_create(user=user)
            context = {
            'user': user, 'token':token, 'client_address': settings.CLIENT_ADDRESS
            }
            send_html_email(
                request,
                'INVITATION TO MUNI RIF SYSTEM AS A REVIEWER',
                [user.username],
                'emails/reviewer-invite.html',
                context
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['PUT'], name='update_reviewer', url_path=r'update-reviewer')
    def update_reviewer(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, id=pk)
        user.username = request.data['email']
        user.email = request.data['email']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.is_active = request.data['is_active']
        user.save()
        profile = user.profile
        profile.faculty_id=request.data['faculty']
        profile.department_id=request.data['department']
        profile.qualification_id=request.data['qualification']
        profile.phone=request.data['phone']
        profile.gender=request.data['gender']
        profile.designation=request.data['designation']
        profile.save()

        theme_ids = request.data.get('themes')
        ProfileTheme.objects.filter(profile=profile).exclude(theme_id__in=theme_ids).delete()
        for theme_id in theme_ids:
            if not ProfileTheme.objects.filter(theme_id=theme_id, profile=profile):
                ProfileTheme.objects.create(theme_id=theme_id, profile=profile)

        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
        

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
            profile = user.profile
            profile.user=user
            profile.faculty_id=request.data['faculty']
            profile.department_id=request.data['department']
            profile.qualification_id=request.data['qualification']
            profile.phone=request.data['phone']
            profile.gender=request.data['gender']
            profile.designation=request.data['designation']
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
            profile = user.profile
            profile.faculty_id=request.data['faculty']
            profile.department_id=request.data['department']
            profile.qualification_id=request.data['qualification']
            profile.phone=request.data['phone']
            profile.gender=request.data['gender']
            profile.designation=request.data['designation']

            login(request, user)

            user_data = UserSerializer(user).data
            user_data['groups'] = [group.name for group in user.groups.all()]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user_data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

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
def update_user(request):
    serializer = UpdateUserSerializer(data=request.data)
    if serializer.is_valid():
        token = Token.objects.get(key=request.data['token'])
        user = token.user
        data = request.data
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['username']
        user.username = data['username']
        user.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.faculty_id = data['faculty']
        profile.department_id = data['department']
        profile.qualification_id = data['qualification']
        profile.designation = data['designation']
        profile.phone = data['phone']
        profile.save()
        
        user_data = UserSerializer(user).data
        user_data['groups'] = [group.name for group in user.groups.all()]
        return Response({'token': token.key, 'user': user_data})
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
            'emails/password-reset-1.html',
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
