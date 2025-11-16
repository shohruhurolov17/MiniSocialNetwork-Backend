from django.db import models
from apps.shared.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )

    full_name = models.CharField(
        _('full name'),
        max_length=255
    )

    username = models.TextField(
        _('username'),
        unique=True
    )

    email = models.EmailField(
        _('email address'),
        unique=True
    )

    is_verified = models.BooleanField(
        _('verified'),
        default=False
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )

    is_active = models.BooleanField(
        _('active'),
        default=True
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:

        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-created_at', )
        indexes = [
            models.Index(
                fields=['username']
            ),
            models.Index(
                fields=['email']
            )
        ]

