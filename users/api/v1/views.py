from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from rest_framework import permissions
# from rest_framework_simplejwt.views import TokenObtainPairView
# from users.api.v1.serializers import CustomTokenObtainPairSerializer, CustomSocialLoginSerializer


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#     token_obtain_pair = TokenObtainPairView.as_view()
#     permission_classes = [permissions.AllowAny]


class FacebookLoginAPI(SocialLoginView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    adapter_class = FacebookOAuth2Adapter

    def post(self, request, *args, **kwargs):
        request_type = self.request.GET.get("type")
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        response = self.get_response()
        try:
            if request_type == "login":
                profile = response.data.get("user_detail")
                if any([profile.get("timezone"), profile.get("phone_number"), profile.get("country_code")]):
                    response.data["registered"] = True
        except:pass
        return response


class GoogleLoginAPI(SocialLoginView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        request_type = self.request.GET.get("type")
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        response = self.get_response()
        try:
            if request_type == "login":
                profile = response.data.get("user_detail")
                if any([profile.get("timezone"), profile.get("phone_number"), profile.get("country_code")]):
                    response.data["registered"] = True
        except:pass
        return response


class FacebookLoginConnectAPI(SocialConnectView):
    authentication_classes = []
    permission_classes = []
    adapter_class = FacebookOAuth2Adapter


class GoogleLoginConnectAPI(SocialConnectView):
    authentication_classes = []
    permission_classes = []
    adapter_class = GoogleOAuth2Adapter