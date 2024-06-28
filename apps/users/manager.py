from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Password is required")
        if not phone:
            raise ValueError("Phone number is required")
        
        email = email.lower()
        phone = phone.title()

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            **extra_fields
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_active = True

        # Set email verification fields
        user.is_email_verified = True
        user.email_verified_at = timezone.now()

        # Set phone verification fields
        user.is_phone_verified = True
        user.phone_verified_at = timezone.now()

        user.save(using=self._db)
        return user
