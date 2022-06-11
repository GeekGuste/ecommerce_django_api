from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN = 'ADMIN'
SUPERADMIN = 'SUPERADMIN'
ROLES = [(ADMIN, 'ADMIN'), (SUPERADMIN, 'SUPERADMIN'),]

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=15,choices=ROLES, null=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number', 'role']
