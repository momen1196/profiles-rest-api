import email
from operator import mod
from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    '''Manager for user profile'''

    def create_user(self, email, name, password=None):
        '''Return a created user 
        Create a new user profile
        '''
        if not email:
            raise ValueError('Users must have an email address!')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    @transaction.atomic
    def create_superuser(self, email, name, password):
        '''Return a created super_user 
        Create and save a new superuser with given details
        '''
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''
    Database model for users in the system
    '''
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    @property
    def full_name(self) -> str:
        '''
        Retrieve full name of user
        '''
        return self.name.capitalize()

    def __str__(self) -> str:
        return self.email.split('@')[0]

    def __repr__(self) -> str:
        return self.email.split('@')[0]
