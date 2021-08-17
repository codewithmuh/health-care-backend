import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models import Q
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import ugettext_lazy as _


class APKBuild(models.Model):
    version = models.CharField(max_length=255)
    apk = models.FileField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.version)

    class Meta:
        verbose_name_plural = 'APK Builds'
        ordering = ('-created',)


class User(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
    )
    image = models.ImageField(upload_to="profile/", null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="male")
    credits = models.PositiveIntegerField(default=10)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        verbose_name_plural = 'Users'
        ordering = ('-date_joined',)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'username': reset_password_token.user.get_full_name,
        'reset_password_token': reset_password_token.key
    }
    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Health Care"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


