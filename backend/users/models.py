from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import (
    AbstractUser, PermissionsMixin, UserManager,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, email, password, first_name, last_name, username, **extra_fields
    ):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('У пользователя должен быть username')
        if not email:
            raise ValueError('У пользователя должен быть email')
        if not first_name:
            raise ValueError('У пользователя должно быть имя')
        if not last_name:
            raise ValueError('У пользователя должна быть фамилия')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            last_name=last_name,
            first_name=first_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email, username, first_name, last_name, password, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )

    def create_superuser(
        self, email, username=None, first_name=None, last_name=None,
        password=None, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )

    def create_staffuser(
        self, username, first_name=None, last_name=None, email=None, password=None
    ):
        user = self.create_user(
            username,
            password,
            first_name,
            last_name,
            email,
            is_staff=True,
            is_admin=False
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True) # тут активировать только после нажатия на ссылку
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):

        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
