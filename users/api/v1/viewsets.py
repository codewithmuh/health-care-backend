from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from users.models import APKBuild
from users.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    UserProfileSerializer,
    APKBuildSerializer, ReSendSerializer
)


User = get_user_model()


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.none()
    http_method_names = ["post", "option"]

    @swagger_auto_schema(request_body=ReSendSerializer)
    @action(methods=['post'], detail=False, url_path='re-send', url_name='re-send')
    def re_send(self, request, *args, **kwargs):
        response = "Email sent!"
        serializer = ReSendSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(response)


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    http_method_names = ["get", "patch"]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first(), many=False)
        return Response(serializer.data)


class APKBuildViewSet(ReadOnlyModelViewSet):
    queryset = APKBuild.objects.all()
    serializer_class = APKBuildSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first(), many=False)
        return Response(serializer.data)

