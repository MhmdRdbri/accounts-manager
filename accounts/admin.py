from django.contrib import admin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "is_admin", "is_staff", "is_superuser")
    search_fields = ("phone_number", "is_admin", "is_staff")
    list_filter = ("is_admin", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("phone_number",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("age", "fullname", "email", "username")
    search_fields = ("user__phone_number", "fullname", "email", "username")
    list_filter = ("age",)
    ordering = ("user__phone_number",)
