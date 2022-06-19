from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name=None, user_image=None, gender=None, address=None, phone=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_user = True
        user.user_image = user_image
        user.name = name
        user.phone = phone
        user.gender = gender
        user.address = address
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
    selections = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField('Name', max_length=150, null=True)
    user_image = models.ImageField(upload_to='user_image/', blank=True)
    phone = models.PositiveBigIntegerField('Phone Number', unique=True, null=True)
    gender = models.CharField('Gender', max_length=20, choices=selections, default='Male', null=True)
    address = models.CharField('Address', max_length=80, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

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

    def get_gender(self):
        if not self.gender:
            return 'Male'
        else:
            return self.gender

    def get_image(self):
        if not self.user_image:
            return '/media/user_image/user.jpg'
        else:
            return self.user_image
