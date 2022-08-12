from email import message
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, 
        write_only=True, 
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        max_length=255, 
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": _('Passwords must match.'), 
                "confirm_password": _('Passwords must match.')
            })

        return attrs

    def save(self, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='Email is not available.')
        ]
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileUpdateSerializer(UserProfileSerializer):
    def to_representation(self, instance):
        return { 
            "id": instance.id,
            "username" : instance.username,
            "account_type": self.context['request'].account_perm.name,
            "allow_download": self.context['request'].account_perm.allow_download,
        }