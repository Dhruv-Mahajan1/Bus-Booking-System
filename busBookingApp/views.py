import datetime
import string
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BusSerializer, SeatBookingSerializer, BusUserSerializer
import pandas as pd
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Bus, SeatBooking, BusUser
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout


class AddBusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = BusSerializer(data=request.data)   
        bususer = BusUser.objects.get(user=request.user)
        if bususer.userType=="admin":
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to add bus."}, status=status.HTTP_401_UNAUTHORIZED)
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        bus = Bus.objects.get(pk=pk)
        serializer = BusSerializer(bus, data=request.data)
        bususer = BusUser.objects.get(user=request.user)
        if bususer.userType=="admin":
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to update bus."}, status=status.HTTP_401_UNAUTHORIZED)
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        bus = Bus.objects.get(pk=pk)
        bususer = BusUser.objects.get(user=request.user)
        if bususer.userType=="admin":
            bus.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete bus."}, status=status.HTTP_401_UNAUTHORIZED)
class SingleBusDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            bus = Bus.objects.get(pk=pk)
            serializer = BusSerializer(bus)
            return Response(serializer.data)
        except Bus.DoesNotExist:
            return Response({'error': 'Bus does not exist'}, status=status.HTTP_404_NOT_FOUND)

class AvailableBusesView(APIView):
    def get(self, request, source, destination, format=None):
        buses = Bus.objects.filter(source=source, destination=destination)
        serializer = BusSerializer(buses, many=True)
        for data, bus in zip(serializer.data, buses):
            booked_seats_count = SeatBooking.objects.filter(bus=bus.id).count()
            print(booked_seats_count)
            data['available_seats'] = bus.total_seats - booked_seats_count
        return Response(serializer.data)

class SeatAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, bus_id, format=None):
        try:
            bus = Bus.objects.get(pk=bus_id)
            total_seats = bus.total_seats
            booked_seats = SeatBooking.objects.filter(bus=bus, booking_status=True).values_list('seat_number', flat=True)
            available_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]
            print(available_seats)
            return Response({
                'bus_id': bus_id,
                'total_seats': total_seats,
                'available_seats': available_seats,
            })
        except Bus.DoesNotExist:
            return Response({'error': 'Bus does not exist'}, status=status.HTTP_404_NOT_FOUND)
    permission_classes = [IsAuthenticated]
    def post(self, request, bus_id, format=None):
        try:
            seat_number = request.data.get('seat_number')
            bus = Bus.objects.select_for_update().get(pk=bus_id)  # Lock the bus record for update

            if seat_number in SeatBooking.objects.filter(bus=bus, booking_status=True).values_list('seat_number', flat=True):
                return Response({'error': 'Seat is already booked'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the seat is already booked by another user within the database transaction
            if SeatBooking.objects.filter(bus=bus, seat_number=seat_number, booking_status=True).exists():
                return Response({'error': 'Seat is already booked'}, status=status.HTTP_400_BAD_REQUEST)

            new_booking = SeatBooking.objects.create(
                user=request.user,
                bus=bus,
                seat_number=seat_number,
                booking_status=True
            )
            new_booking.save()

            return Response({'message': f'Seat {seat_number} successfully booked'}, status=status.HTTP_200_OK)
        except Bus.DoesNotExist:
            return Response({'error': 'Bus does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UserSeatBookingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,format=None):
        try:
            user_bookings = SeatBooking.objects.filter(user=request.user, booking_status=True)
            serializer = SeatBookingSerializer(user_bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelSeatBookingView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, booking_id, format=None):
        try:
            booking = SeatBooking.objects.get(pk=booking_id)

            # Check if the request user matches the user who booked the seat
            if booking.user != request.user:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            booking.booking_status = False  # Set booking_status to False (cancel the booking)
            booking.save()

            return Response({'message': 'Seat booking canceled successfully'}, status=status.HTTP_200_OK)
        except SeatBooking.DoesNotExist:
            return Response({'error': 'Booking does not exist'}, status=status.HTTP_404_NOT_FOUND)

class BusUserLoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Logged in successfully.",'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class BusUserRegistrationAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            print("Username already taken")
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            print("email already taken")
            return Response({"error": "Email already taken."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=data.get('password'), email=email)
        print("user created",user)
        teacher=BusUser.objects.create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        print("token created",token)
        return Response({"message": "Logged in successfully.",'token': token.key}, status=status.HTTP_200_OK)

class BusUserLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user

        serializer = BusUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)