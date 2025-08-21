from rest_framework import serializers
from .models import Profile, Ride
from django.contrib.auth.models import User
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'origin', 'destination', 'fare', 'ride_time']
        read_only_fields = ['id', 'ride_time']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'phone_number']
        read_only_fields = ['user']

        
