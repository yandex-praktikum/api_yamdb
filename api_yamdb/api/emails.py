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


def send_confirmation_code(email, confirmation_code):
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'your_email@example.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False)
