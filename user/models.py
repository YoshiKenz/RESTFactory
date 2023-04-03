from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, app, app_role, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, app_role=app_role, username=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        print("CustomUserManager " + user.__str__())
        return user

    def create_superuser(self, email, app, app_role):

        try:
            user = CustomUser.objects.get(email=email)
            app_roles = user.app_role.split(', ')
            if f'{app_role}_{app}' not in app_roles:
                user.app_role = ', '.join(user.app_role, f'{app_role}_{app}')
                user.is_superuser = True
        except CustomUser.DoesNotExist:
            user = self.create_user(
                email=self.normalize_email(email),
                app_role=app_role,
                is_superuser=True,
            )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    app_role = models.TextField(blank=True, default="")

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.email
