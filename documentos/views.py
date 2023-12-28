
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Documento, Permissao
from .serializers import DocumentoSerializer, UserSerializer    
from rest_framework.parsers import MultiPartParser, FormParser

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):
        if Permissao.objects.filter(usuario=request.user, permissao='R').exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response({"error": "User has no permission to read"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def retrieve(self, request, *args, **kwargs):
        if Permissao.objects.filter(usuario=request.user, permissao='R').exists():
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"error": "User has no permission to read"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def create(self, request, *args, **kwargs):
        if Permissao.objects.filter(usuario=request.user, permissao='W').exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "User has no permission to write"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def update(self, request, *args, **kwargs):
        if Permissao.objects.filter(usuario=request.user, permissao='W').exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response({"error": "User has no permission to write"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, *args, **kwargs):
        if Permissao.objects.filter(usuario=request.user, permissao='W').exists():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"error": "User has no permission to write"}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=True, methods=['get'])
    def verify(self, request, pk=None):
        if Permissao.objects.filter(usuario=request.user, permissao='C').exists():
            documento = self.get_object()
            if documento.check_hash():
                return Response({"message": "The hash is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The hash is not valid"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User has no permission to verify"}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserViewSet(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class SignInView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }
    ))
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username/password."}, status=status.HTTP_400_BAD_REQUEST)
        
class SignUpView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'permission': openapi.Schema(type=openapi.TYPE_STRING, description='permission'),
        }
    ))
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        permission = request.data.get("permission")
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password, email=email)
            Permissao.objects.create(usuario=User.objects.get(username=username), permissao=permission)
            return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)