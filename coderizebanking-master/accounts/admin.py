from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in displaying the CustomUser model
    model = CustomUser
    list_display = ['mobile_number', 'first_name', 'last_name', 'role','is_approved','is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['mobile_number', 'first_name', 'last_name']
    ordering = ['mobile_number']

    # The fields to be used in adding/editing a user
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_approved')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('mobile_number', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # These methods define how passwords are set/changed
    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing user
            return super().get_fieldsets(request, obj)
        else:  # Adding a new user
            return self.add_fieldsets

    def save_model(self, request, obj, form, change):
        obj.save()

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
