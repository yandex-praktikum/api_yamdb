from rest_framework.views import APIView

from .models import User
from .utils import generate
from .serializers import (
    RegisterSerializer,
    UserSerializer
)
from .permissions import (
    IsAdmin,
    IsModerator,
    IsAuthor
)


class RegisterAPIView(APIView):
    """ View для регистрации """
    register_serializer = RegisterSerializer
    user_serializer = UserSerializer

    def post(self, request):
        data = self.register_serializer(data=request.data)
        if data.is_valid():
            username = data.validated_data.get('username')
            email = data.validated_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                code = user.confirmation_code
            else:
                code = generate()
                data = {
                    'username': username,
                    'email': email,
                    'confirmation_code': code
                }
                user = self.user_serializer(data=data)
