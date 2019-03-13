from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=20)
    message = models.TextField(blank=False)
    def __str__(self):
        return self.subject

class Feedback(models.Model):
    pass