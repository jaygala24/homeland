from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name


class Feedback(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.user.name
