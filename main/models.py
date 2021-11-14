from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True
    """
    커스텀 유저모델 매니저 (고유 이메일)
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=10, blank=False, null=True)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    # place
    # course_like = models.ManyToManyField("place.Place", related_name='course_likes',blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Admin 계정 접속을 위한 Boolean 필드'),
    )

    USERNAME_FIELD = 'email'
    email.db_index = True
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'password']
    objects = UserManager()

    def __str__(self):
        return self.email
