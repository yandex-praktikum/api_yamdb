from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(self.make_random_password(
            length=8, allowed_chars='0123456789'))
        user.save()
        return user
