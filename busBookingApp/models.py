from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    available_days = models.CharField(max_length=100)  # Store days of operation as needed
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    fare = models.IntegerField()

class SeatBooking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_status = models.BooleanField(default=False)
    booking_date = models.DateField(auto_now_add=True)
    booking_time = models.TimeField(auto_now_add=True)
    
class BusUser(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userType=models.CharField(max_length=100,default="user")
    def __str__(self):
        return self.user.username
    
