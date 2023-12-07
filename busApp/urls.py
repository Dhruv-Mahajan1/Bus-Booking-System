from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from busBookingApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buses/', views.AddBusView.as_view(), name='bus-list'),  # Endpoint for getting all buses and creating a new bus
    path('buses/<int:pk>/', views.AddBusView.as_view(), name='bus-detail'),  # Endpoint for updating and deleting a specific bus
    path('busDetail/<int:pk>/', views.SingleBusDetailView.as_view(), name='busdetails'),
    path('buses/available/<str:source>/<str:destination>/', views.AvailableBusesView.as_view(), name='available-buses'),  # Endpoint for available buses
    path('buses/seat_availability/<int:bus_id>/', views.SeatAvailabilityView.as_view(), name='seat-availability'),  # Endpoint for seat availability
    path('buses/cancel_booking/<int:booking_id>/', views.CancelSeatBookingView.as_view(), name='cancel-booking'),  # Endpoint for cancelling seat booking
    path('buses/viewBookedseats/', views.UserSeatBookingView.as_view(), name='viewBookedseats'),  # Endpoint for booking a seat
    path('login/', views.BusUserLoginAPI.as_view(), name='user-login'),  # Endpoint for user login
    path('signup/', views.BusUserRegistrationAPI.as_view(), name='user-registration'),  # Endpoint for user registration
    path('logout/', views.BusUserLogoutAPI.as_view(), name='logout'),
    path('userInfo/', views.UserInfo.as_view(), name='userInfo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)