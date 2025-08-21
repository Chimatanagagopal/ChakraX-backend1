
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    ride_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.origin} to {self.destination}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=20)      
    email = models.EmailField(max_length=255)         
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.id} - {self.username} - {self.email} - {self.phone_number}"
