from django.contrib.auth.models import BaseUserManager, UserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_kwargs):

        if not email:
            
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_kwargs):

        extra_kwargs.setdefault('is_staff', True)
        extra_kwargs.setdefault('is_superuser', True)
        extra_kwargs.setdefault('is_active', True)

        if extra_kwargs.get('is_staff') is not True:
            raise ValueError('SuperUser must have is_staff=True')
        
        if extra_kwargs.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser=True')
        
        return self.create_user(
            email,
            password,
            **extra_kwargs
        )