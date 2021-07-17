from django.contrib.auth.models import AbstractUser
from django.db.models import (CharField, CheckConstraint, EmailField, F, Q,
                              TextField)
from django.utils.translation import gettext_lazy as _

from .managers import APIUserManager

only_admin = Q(role='admin') & Q(is_staff=True)
only_not_admin = Q(role__in=('user', 'moderator')) & Q(is_staff=False)


class User(AbstractUser):
    CHOICES = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'админ')
    )
    username = CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        validators=(AbstractUser.username_validator,),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = EmailField('Email', unique=True)
    role = CharField('Роль', default='user', max_length=9, choices=CHOICES)
    bio = TextField('Биография', blank=True)

    objects = APIUserManager()

    USERNAME_FIELD = 'id'

    class Meta(AbstractUser.Meta):
        constraints = (
            CheckConstraint(
                name='only-admin-must-be-staff',
                check=only_admin | only_not_admin
            ),
        )

    def __str__(self):
        return str(self.pk)
