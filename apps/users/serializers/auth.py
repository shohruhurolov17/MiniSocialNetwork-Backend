from rest_framework import serializers
from apps.users.models import CustomUser
import re


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser
        fields = (
            'full_name',
            'username',
            'email',
            'password'
        )
    
    def validate_username(self, val):

        if len(val) <= 5 or len(val) >= 1000:
            raise serializers.ValidationError('Username must be longer than 5 and shorter than 1000 characters')

        return val

    def validate_full_name(self, val):

        if not re.match(
            r'^[A-Za-zА-Яа-яЁё\s]+$',
            val
        ):
            raise serializers.ValidationError('Fullname may contain only Latin/Cyrillic letters and spaces')

        return val
    
    def create(self, validated_data):

        return CustomUser.objects.create_user(**validated_data)