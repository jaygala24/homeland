from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

PHONE_REGEX = r'^\+?1?\d{9,14}$'


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        """
        Creates and saves a User with the given email, name, phone
        and password
        """
        if not email:
            raise ValueError('Email is required')
        if not name:
            raise ValueError('Name is required')
        if not phone:
            raise ValueError('Phone is required')
        if not password:
            raise ValueError('Password is required')
        user = self.model(
            email=email, name=name, phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, phone, password=None):
        """
        Creates and saves a Staffuser with the given email, name, phone
        and password
        """
        user = self.create_user(email, name, phone, password=password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        """
        Creates and saves a Superuser with the given email, name, phone
        and password
        """
        user = self.create_user(email, name, phone, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[
                             RegexValidator(regex=PHONE_REGEX)])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    token = models.CharField(max_length=10, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', ]

    objects = UserManager()

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
