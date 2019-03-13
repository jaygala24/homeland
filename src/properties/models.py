from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def upload_location(instance, filename):
    return f"{instance.realtor}/{instance.title}/{filename}"


class Property(models.Model):
    realtor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Mumbai')
    state = models.CharField(max_length=100, default='Maharashtra')
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20)
    price = models.IntegerField()
    sqft = models.IntegerField()
    photo_main = models.ImageField(upload_to=upload_location)
    photo_1 = models.ImageField(upload_to=upload_location, blank=True)
    photo_2 = models.ImageField(upload_to=upload_location, blank=True)
    photo_3 = models.ImageField(upload_to=upload_location, blank=True)
    photo_4 = models.ImageField(upload_to=upload_location, blank=True)
    photo_5 = models.ImageField(upload_to=upload_location, blank=True)
    status = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
