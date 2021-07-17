from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager


class APIUserManager(UserManager):

    def _create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        username = AbstractUser.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username=None, password=None,
                    **extra_fields):
        if extra_fields.get('role') == 'admin':
            extra_fields['is_staff'] = True
            if not username:
                raise ValueError('Admin must have username')
            if not password:
                raise ValueError('Admin must have password')

        if extra_fields.get('role') in ('user', 'moderator'):
            extra_fields['is_staff'] = False

        extra_fields['is_superuser'] = False

        return self._create_user(email=email, username=username,
                                 password=password, **extra_fields)

    def create_superuser(self, email, username=None, password=None,
                         **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['role'] = 'admin'

        if not username:
            raise ValueError('Superuser must have username')
        if not password:
            raise ValueError('Superuser must have password')

        return self._create_user(email=email, username=username,
                                 password=password, **extra_fields)
