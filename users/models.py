# users/models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you want for the user profile
    email = models.EmailField()
    # Add more fields as needed

    def __str__(self):
        return f'{self.user.username} Profile'
