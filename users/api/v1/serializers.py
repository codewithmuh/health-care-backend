from datetime import date

from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email, send_email_confirmation
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.models import TokenModel

from users.models import APKBuild

User = get_user_model()


class APKBuildSerializer(serializers.ModelSerializer):

    class Meta:
        model = APKBuild
        fields = "__all__"


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    dob = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", 'dob', 'gender')
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {
                "required": True,
                "allow_blank": False,
            }
        }

    def _get_request(self):
        request = self.context.get("request")
        if (
            request
            and not isinstance(request, HttpRequest)
            and hasattr(request, "_request")
        ):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    @transaction.atomic()
    def create(self, validated_data):
        try:
            user = User(
                email=validated_data.get("email"),
                name=validated_data.get("name"),
                dob=validated_data.get("dob"),
                gender=validated_data.get('gender'),
                username=generate_unique_username(
                    [validated_data.get("name"), validated_data.get("email"), "user"]
                ),
            )

            user.set_password(validated_data.get("password"))
            user.save()
            request = self._get_request()
            setup_user_email(request, user, [])
            try:
                send_email_confirmation(request, user, signup=True)
            except Exception as e:
                raise serializers.ValidationError(
                    _(f"error while sending email {e}")
                )
        except Exception as e:
            raise serializers.ValidationError(
                    _(f"error while creating user {e}")
                )
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "image", "credits", "dob", "gender", "age"]

    def get_age(self, obj):
        if obj.dob:
            today = date.today()
            print(obj.dob)
            return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
        return None


class UserProfileSerializer(UserSerializer):
    image = Base64ImageField(required=False)


class CustomTokenSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="user", read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', "user_detail")


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""

    password_reset_form_class = ResetPasswordForm

