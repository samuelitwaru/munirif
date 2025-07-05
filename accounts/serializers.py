# serializers.py
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

from core.serializers import DepartmentSerializer, FacultySerializer, ProfileSerializer, QualificationSerializer

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only (not displayed in responses)
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    

class CustomAuthTokenSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required= True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        errors = {}
        if not User.objects.filter(username=data.get('email')).first():
            errors['email'] = ["This email does not exist."]
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
class CompleteSignupSerializer(serializers.Serializer):
    token = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    # phone = serializers.IntegerField()
    # gender = serializers.CharField()
    # faculty = serializers.IntegerField()
    # department = serializers.IntegerField()
    # qualification = serializers.IntegerField()
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
  

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    
class UpdateUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.IntegerField()
    faculty = serializers.IntegerField()
    department = serializers.IntegerField()
    qualification = serializers.IntegerField()
    