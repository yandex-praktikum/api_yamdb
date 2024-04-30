from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ConfirmationCodeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неверный код подтверждения')

        return (user, None)
