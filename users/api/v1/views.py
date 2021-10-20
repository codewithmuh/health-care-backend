from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from rest_framework import permissions
# from rest_framework_simplejwt.views import TokenObtainPairView
# from users.api.v1.serializers import CustomTokenObtainPairSerializer, CustomSocialLoginSerializer


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#     token_obtain_pair = TokenObtainPairView.as_view()
#     permission_classes = [permissions.AllowAny]


class FacebookLoginAPI(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLoginAPI(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class FacebookLoginConnectAPI(SocialConnectView):
    authentication_classes = []
    permission_classes = []
    adapter_class = FacebookOAuth2Adapter


class GoogleLoginConnectAPI(SocialConnectView):
    authentication_classes = []
    permission_classes = []
    adapter_class = GoogleOAuth2Adapter
