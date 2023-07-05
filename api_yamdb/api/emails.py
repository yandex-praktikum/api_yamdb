from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
        return Response({'error': 'Email или username уже существуют'}, status=400)

    user = User.objects.create(email=email, username=username)
    send_confirmation_code(user.email, user.confirmation_code)

    return Response({'message': 'Регистрация успешна'})


@api_view(['POST'])
def obtain_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    user = User.objects.filter(username=username, confirmation_code=confirmation_code).first()

    if not user:
        return Response({'error': 'Invalid username or confirmation code'}, status=400)

    # Генерация JWT-токена
    token = user.generate_jwt_token()

    return Response({'token': token})

def send_confirmation_code(email, confirmation_code):
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'your_email@example.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False)
