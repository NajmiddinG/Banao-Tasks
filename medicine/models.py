from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_field):
        if not username:
            raise ValueError('User must have username address.')
        user = self.model(username=username, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="First name", max_length=50)
    last_name = models.CharField(verbose_name="Last name", max_length=50)
    picture = models.ImageField(verbose_name="Image", upload_to="Users/", blank=True, null=True)
    username = models.CharField(verbose_name="Username", max_length=50, unique=True)
    email = models.EmailField(verbose_name="Email", unique=True)
    address = models.TextField(verbose_name="Adress(line1, city, state, pincode)", max_length=500)
    class type_choise(models.TextChoices):
        Patient = 'P', _('Patient')
        Doctor = 'D', _('Doctor')
    type = models.CharField(
        verbose_name="Type", choices=type_choise.choices, default=type_choise.Patient, max_length=2)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

