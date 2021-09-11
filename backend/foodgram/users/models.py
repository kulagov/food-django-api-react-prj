from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address')
