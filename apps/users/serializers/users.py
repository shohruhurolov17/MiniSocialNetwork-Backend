from rest_framework import serializers
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserDetailSerializer(serializers.ModelSerializer):

    refresh_token = serializers.SerializerMethodField()
    access_token = serializers.SerializerMethodField()

    class Meta:

        model = CustomUser
        fields = (
            'refresh_token',
            'access_token',
            'id',
            'full_name',
            'email',
            'is_verified',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'refresh_token',
            'access_token',
            'is_verified'
        )

    def get_refresh_token(self, instance) -> str:

        return str(RefreshToken.for_user(instance))
    
    def get_access_token(self, instance) -> str:

        return str(RefreshToken.for_user(instance).access_token)
