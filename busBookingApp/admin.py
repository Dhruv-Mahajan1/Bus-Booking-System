from django.contrib import admin


from .models import *

admin.site.register(Bus)
admin.site.register(SeatBooking)
admin.site.register(BusUser)