ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
USER_ROLES_CHOICES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор'),
)
EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 150
ROLE_MAX_LENGTH = max(len(role[0]) for role in USER_ROLES_CHOICES)
