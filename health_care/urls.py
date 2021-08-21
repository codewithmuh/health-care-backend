from allauth.account.views import confirm_email
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static

# swagger
api_info = openapi.Info(
    title="Health Care API",
    default_version="v1",
    description="API documentation for Health Care App",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = []

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]



urlpatterns += [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    # Override email confirm to use allauth's HTML view instead of rest_auth's API view
    path("rest-auth/registration/account-confirm-email/<str:key>/", confirm_email),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("api/v1/", include([
        path("", include("users.api.v1.urls")),
        path("", include("subscription.urls")),
        path("", include('backapi.api.v1.urls')),
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
