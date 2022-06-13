from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_user = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        staff = self.model(
            email=self.normalize_email(email),
        )
        staff.set_password(password)
        staff.is_staff = True
        staff.save(using=self._db)
        return staff

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_user = False
        user.save(using=self._db)
        return user


class UserEmail(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    has_data = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def admin(self):
        "Is the user a admin member?"
        return self.is_admin


class UserDetails(models.Model):
    selections = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
    name = models.CharField('Name', max_length=150)
    user_image = models.ImageField(upload_to='user_image/')
    age = models.PositiveSmallIntegerField('Age')
    phone = models.PositiveBigIntegerField('Phone Number', unique=True)
    gender = models.CharField('Gender', max_length=20, choices=selections)
    address = models.CharField('Address', max_length=80)
    email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)

    def __str__(self):
        return self.email.email
