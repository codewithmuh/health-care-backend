from django.db import models


class CreditsSetting(models.Model):
    credits = models.PositiveIntegerField(verbose_name="Credits per dollar")

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.credits)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "1- Credits Per Dollar"
