from django.db.models.fields import EmailField
from rest_framework import serializers
from .models import CostumUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostumUser
        fields = '__all__'

    def create(self, validated_data):
        return CostumUser.objects.create(
            email=validated_data['email']
        )


class GetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumUser
        fields = '__all__'


class CodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=1000)
    email = serializers.EmailField()