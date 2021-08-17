from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_auth.views import LoginView, PasswordChangeView

# from users.api.v1.views import FacebookLoginAPI, GoogleLoginAPI
from users.api.v1.viewsets import (
    SignupViewSet,
    UserProfileViewSet,
    APKBuildViewSet,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("profile", UserProfileViewSet, basename="user_profile")
router.register("apk", APKBuildViewSet, basename="province-name")

urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('forgot-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    # path('login/facebook/', FacebookLoginAPI.as_view(), name='fb_login'),
    # path('login/google/', GoogleLoginAPI.as_view(), name='google_login'),
]
