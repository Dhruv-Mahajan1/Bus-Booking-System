from rest_framework import serializers
from .models import BusUser, Bus,SeatBooking

class BusUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusUser
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    class Meta:
        model = Bus
        fields = ['id', 'name', 'total_seats', 'departure_time', 'arrival_time', 'source', 'destination', 'available_seats',
                    'fare', 'available_days',
                    'current_occupancy'
                    ]
                  
    def get_available_seats(self, obj):
        booked_seats_count = SeatBooking.objects.filter(bus=obj).count()
        print(booked_seats_count)
        print(obj.total_seats)
        return obj.total_seats - booked_seats_count

class SeatBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatBooking
        fields = '__all__'
