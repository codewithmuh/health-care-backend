from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.models import APKBuild

from users.forms import UserChangeForm, UserCreationForm


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",
                                      "image", "dob", "gender", 'credits')}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "email", "name", "is_superuser", 'gender', 'dob', 'credits']
    search_fields = ["name", "email"]


class APKBuildAdmin(admin.ModelAdmin):
    list_display = ('version', "created")


admin.site.register(APKBuild, APKBuildAdmin)


