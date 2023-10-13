from django.db import models
from django.contrib.auth.models import User

class NewProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='default_name')
    email = models.EmailField(max_length=255, default='default_email@example.com')

    def __str__(self):
        return self.user.username
