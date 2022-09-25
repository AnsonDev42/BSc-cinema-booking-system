import secrets
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ########################## DO NOT CHANGE ##########################
    # Django default user fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    # User's privileges
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    ###################################################################

    # Extended fields
    # TODO: we might want to change nullable to false
    birthday = models.DateField(null=True)
    verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=256, default=secrets.token_hex(32))

    # TODO: add more fields in the future

    USERNAME_FIELD = 'email'    # Changing login field to use email instead of username
    REQUIRED_FIELDS = ['username']

    objects = UserAccountManager()

    def __str__(self):
        return self.email

    def generate_auth_token(self):
        """
        Create a new authentication token for verification.
        """
        self.auth_token = secrets.token_hex(32)
        self.save()
        return self.auth_token

    def verify_user(self, token):
        """
        Checks if the incoming token matches authentication token.
        Return true if same.
        """
        if token == self.auth_token:
            self.verified = True
        return self.verified


    ########################## DO NOT CHANGE ##########################
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    ###################################################################
