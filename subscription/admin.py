from django.contrib import admin
from .models import CreditsSetting
# Register your models here.


@admin.register(CreditsSetting)
class CreditsSettingAdmin(admin.ModelAdmin):
    list_display = ['credits', 'last_updated', 'created']
    list_per_page = 50
