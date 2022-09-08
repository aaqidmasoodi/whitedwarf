from django.contrib import admin
from .models import Bus, Alert


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):

    readonly_fields = ["location_broadcast_id"]


admin.site.register(Alert)
