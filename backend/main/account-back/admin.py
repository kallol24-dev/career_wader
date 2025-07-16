from django.contrib import admin






# from django.contrib import admin
from .models import Admin, User

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone", "role", "country", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone")
    list_filter = ("role", "country", "is_staff", "is_active")
    ordering = ("email",)


    # Keep "user_permissions" but remove "groups"
    filter_horizontal = ("user_permissions",)

    def get_form(self, request, obj=None, **kwargs):
        """Remove 'groups' and 'is_staff' from the form fields."""
        form = super().get_form(request, obj, **kwargs)
        for field in ["groups", "is_staff", "last_login","is_superuser"]:   #Remove the specific fields
            if field in form.base_fields:
                del form.base_fields[field]
        return form    
        
    
class BaseUserAdmin(admin.ModelAdmin):
    """Base admin for models with a OneToOneField to User"""

    def user_email(self, obj):
        return obj.user.email

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    def user_phone(self, obj):
        return obj.user.phone

    user_email.short_description = "Email"
    user_first_name.short_description = "First Name"
    user_last_name.short_description = "Last Name"
    user_phone.short_description = "Phone"

    list_display = ("user_email", "user_first_name", "user_last_name", "user_phone")



# @admin.register(Counselor)
# class CounselorAdmin(BaseUserAdmin):
#     pass

# @admin.register(Admin)
# class AdminAdmin(BaseUserAdmin):
#   pass