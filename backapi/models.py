from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Measurement(models.Model):
    CATEGORIES_NAME = (
        ('respiratory', 'Respiratory'),
        ('oxygen', 'Oxygen'),
        ('heart rate', 'Heart Rate'),
        ('temperature', 'Temperature'),
        ('viscosity', 'Viscosity'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORIES_NAME)
    value = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=False)
