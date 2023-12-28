from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="SealPDF API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('documentos.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
