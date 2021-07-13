from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'email', 'role', 'description', 'first_name', 'last_name')
        read_only_fields = ('id', 'role', 'description', 'first_name', 'last_name')
        model = User
