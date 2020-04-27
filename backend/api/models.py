from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
import uuid, datetime

# User model based on AbstractUser, the default user.
class User(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=200)
    role = models.CharField(max_length=200, default='Client')
    created_on = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    address = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.uid) + " - " + self.role + " - " + " - " + self.email
