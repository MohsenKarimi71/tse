from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings

import os
import uuid



# def upload_user_image(instance, filename):
#     name, ext = os.path.splitext(filename)
#     filename = f'{uuid.uuid4()}{ext}'
#     return os.path.join(f'account/{instance.user.id}/images/', filename)


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class RoleMixin(models.Model):
    is_superuser = models.BooleanField(
        verbose_name=("Is top manager?"),
        default=False,
    )
    is_staff = models.BooleanField(
        verbose_name=("Is site admin?"),
        default=False,
    )

    @property
    def is_top_manager(self):
        return self.is_superuser

    @is_top_manager.setter
    def is_top_manager(self, status):
        self.is_superuser = status

    @property
    def is_site_admin(self):
        return self.is_staff

    @is_site_admin.setter
    def is_site_admin(self, status):
        self.is_staff = status

    date_joined = models.DateTimeField(
        ("date joined"),
        default=timezone.now
    )

    class Meta:
        abstract = True


class Account(AbstractBaseUser, RoleMixin):
    class UserGender(models.TextChoices):
        MALE = "MALE", ("Male")
        FEMALE = "FEMALE", ("Female")

    email = models.EmailField(
        unique=True,
        verbose_name=("Email"),
        max_length=128
    )
    first_name = models.CharField(
        verbose_name=("first name"),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=("last name"),
        max_length=150,
        blank=True
    )
    gender = models.CharField(
        max_length=6,
        verbose_name=("gender"),
        choices=UserGender.choices,
        default=UserGender.MALE
    )
    is_active = models.BooleanField(
        verbose_name=("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")
        ordering = []

    objects = AccountManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email

    def has_perm(self, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

  
# class Profile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name="User"
#     )
#     image = models.ImageField(
#         verbose_name=("Profile Image"),
#         upload_to=upload_user_image,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = ("Profile")
#         verbose_name_plural = ("Profiles")

#     def __str__(self):
#         return f'{("profile of")} {str(self.user)}'
