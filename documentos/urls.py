from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, UserViewSet, SignInView, SignUpView
from django.urls import path, include
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet, basename='documento')
urlpatterns = router.urls

urlpatterns += [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/', UserViewSet.as_view(), name='user'),
]