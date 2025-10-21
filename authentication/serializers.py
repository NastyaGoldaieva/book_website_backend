from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_check')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Password must contain uppercase letter")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain digit")

        return value

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password_check": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')