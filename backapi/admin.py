from django.contrib import admin
from .models import Measurement, DeductCreditSetting


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'value', 'created']


@admin.register(DeductCreditSetting)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['amount', 'updated', 'created']
