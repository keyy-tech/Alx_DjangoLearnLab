from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Unregister the original User admin
admin.site.unregister(User)

# Register the new User admin with profile inline
admin.site.register(User, UserAdmin)
