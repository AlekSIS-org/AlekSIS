from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
