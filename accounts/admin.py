from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PhoneOTP, Profile


class UserModelAdmin(BaseUserAdmin):
    list_display = ("id", "phone", "name", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("phone", "password")}),
        ("Bus Details", {"fields": ("bus",)}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("phone",)
    ordering = ("phone", "id")
    filter_horizontal = ()


admin.site.register(User, UserModelAdmin)
admin.site.register(PhoneOTP)
admin.site.register(Profile)
