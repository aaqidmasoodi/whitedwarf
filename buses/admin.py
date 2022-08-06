from django.contrib import admin
from .models import Bus, Driver, Passenger


admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Passenger)