from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxValueValidator, MinValueValidator

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.manager import UserManager
from django.utils.text import slugify
import uuid

import datetime
import secrets
import random
from django.utils import timezone

## Custom 
from apps.core.models import TimestampedModel
from apps.users.validators import DateOfBirthValidator, ImageValidator



## AbstructBaseUser has provite some default field ( password, last_login, is_active )
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):

    class GenderType(models.TextChoices):
        MALE   = 'Male', 'male'
        FEMALE = 'Female', 'female'
        OTHERS  = 'Others', 'others'

    class ReligionType(models.TextChoices):
        ISLAM = 'Islam', 'islam'
        HINDU = 'Hindu ', 'hindu'
        CHRISTIAN = 'Christian', 'christian'
        BUDDHIST  = 'Buddhist', 'buddhist'
        OTHERS = 'Others', 'others'

    class AuthProvider(models.TextChoices):
        LOCAL     = 'Local', 'local'
        GOOGLE    = 'Google', 'google'
        TWITTER   = 'Twitter', 'twitter'
        FACEBOOK  = 'Facebook', 'facebook'
        INSTAGRAM = 'Instagram', 'instagram'

    id        = models.UUIDField(
                    verbose_name="ID", 
                    primary_key = True, 
                    unique=True, 
                    default = uuid.uuid4, 
                    editable=False 
                )
    
    slug      = models.SlugField(
                    verbose_name="Slug", 
                    unique=True, 
                    blank=True, 
                    null=True
                )

    email     = models.EmailField(
                    verbose_name="Email address",
                    unique=True,
                    max_length=255,
                    validators=[EmailValidator(message="Enter a valid email address.")],
                )
    phone     = models.CharField(
                    verbose_name="Phone number",
                    unique=True,
                    max_length=30,
                    null = True,
                    blank=True,
                    validators=[
                        RegexValidator(
                            regex=r'^\+?1?\d{9,15}$',
                            message="Phone number must be entered in the format: '+8801XXXXXXXXX'. Up to 15 digits allowed."
                        )
                    ]
                )
    first_name = models.CharField(
                    verbose_name="First name", 
                    max_length=255, 
                    null=True, 
                    blank=True,
                    validators=[MinLengthValidator(2, message="First name must be at least 2 characters long.")]
                )

    last_name  = models.CharField(
                    verbose_name="Last name", 
                    max_length=255, 
                    null=True, 
                    blank=True,
                    validators=[MinLengthValidator(2, message="First name must be at least 2 characters long.")]
                )

    gender = models.CharField(
                verbose_name="Gender", 
                max_length=10, 
                choices=GenderType.choices, 
                null=True, blank=True
            )

    religion = models.CharField(
                verbose_name="Religion", 
                max_length=20, 
                choices=ReligionType.choices, 
                null=True, blank=True
            )
    dob      = models.DateField(
                verbose_name="Date of birth", 
                null=True, 
                blank=True,
                validators=[DateOfBirthValidator]
            ) 

    image    = models.ImageField(
                verbose_name="Profile Image", 
                upload_to="Users/ProfileImage/", 
                null=True, 
                blank=True,
                validators=[ImageValidator]
            )



    ## User Permission and Roll
    is_active   = models.BooleanField(verbose_name="Active", default = True)
    is_admin    = models.BooleanField(verbose_name="Admin", default = False)

    is_email_verified = models.BooleanField(verbose_name="Email Verification", default = False)
    email_verified_at = models.DateTimeField(verbose_name="Email Verification Time", null=True, blank=True)

    is_phone_verified = models.BooleanField(verbose_name="Phone Verification", default = False)
    phone_verified_at = models.DateTimeField(verbose_name="Phone Verification Time", null=True, blank=True)

    is_membership = models.BooleanField(verbose_name="Membership", default = False)

    auth_provider = models.CharField(
                        verbose_name = "Authentication With",
                        max_length=20, 
                        choices=AuthProvider.choices, 
                        default=AuthProvider.LOCAL
                    )

    fcm_device_token = models.TextField(
                        verbose_name = "Device Token", 
                        blank=True,
                        null=True
                    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone']

    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def f_name(self):
        if self.first_name:
            return self.first_name
        return None

    @property
    def l_name(self):
        if self.last_name:
            return self.last_name
        return None

    @property
    def age(self):
        if self.dob:
            # today = datetime.date.today()  ## NOTE:- Automatic Handling of Timezones
            today = timezone.now().date()    ## NOTE:- Integration with Django Settings `TIME_ZONE `

            age   = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        else:
            return None
        
    def save(self, *args, **kwargs):

        ## NOTE:- Save The Slug 
        if not self.slug:
            # base_slug = slugify(f"{self.first_name}-{self.last_name}-{self.email.split('@')[0]}")
            base_slug = slugify(f"{self.email.split('@')[0]}")
            slug = base_slug
            count = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        ## NOTE:- Save email_verified_at when is_email_verified = True
        if self.is_email_verified and not self.email_verified_at:
            self.email_verified_at = timezone.now()
        

        ## NOTE:- Save phone_verified_at when is_phone_verified = True
        if self.is_phone_verified and not self.phone_verified_at:
            self.phone_verified_at = timezone.now()

        super().save(*args, **kwargs)


    class Meta:
        # db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'




class UserOTP(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otp",
        verbose_name="User"
    )

    otp = models.IntegerField(
        verbose_name="OTP Code",
        validators=[
            MinValueValidator(100000, message="OTP must be a 6-digit number."),
            MaxValueValidator(999999, message="OTP must be a 6-digit number.")
        ]
    )

    token = models.CharField(
        verbose_name="Token",
        max_length=100,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9-_]{64}$',
                message="Token must be a valid 64-character string."
            )
        ]
    )

    is_used = models.BooleanField(
        verbose_name="Is Used",
        default=False,
    )

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

    def generate_token(self):
        # generate 64-character token
        token = secrets.token_urlsafe(48)  # 48 bytes give approximately 64 characters when URL-safe encoded
        return token

    def generate_code(self):
        # generate 6-digit OTP
        otp = random.randint(100000, 999999)
        return str(otp).zfill(6)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_code()

        if not self.token:
            self.token = self.generate_token()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User OTP"
        verbose_name_plural = "User OTPs"


