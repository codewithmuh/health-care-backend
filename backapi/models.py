from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Measurement(models.Model):
    CATEGORIES_NAME = (
        ('respiratory', 'Respiratory'),
        ('oxygen', 'Oxygen'),
        ('heart_rate', 'Heart Rate'),
        ('temperature', 'Temperature'),
        ('viscosity', 'Viscosity'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_measurements")
    category = models.CharField(max_length=50, choices=CATEGORIES_NAME)
    value = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ('-created',)


class DeductCreditSetting(models.Model):
    amount = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.amount)

    class Meta:
        ordering = ('-created',)


@receiver(post_save, sender=Measurement)
def deduct_credits_on_measurement(sender, instance, created, **kwargs):
    if created:
        credit_to_deduct = 1
        threshold = DeductCreditSetting.objects.first()
        if threshold:
            credit_to_deduct = threshold.amount
        user = User.objects.filter(pk=instance.user.pk).first()
        if user:
            user.credits = user.credits - credit_to_deduct
            user.save()
