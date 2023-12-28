from rest_framework import serializers
from .models import Documento, User
from rest_framework.response import Response

class DocumentoSerializer(serializers.ModelSerializer):
    pdf = serializers.FileField(write_only=True)

    class Meta:
        model = Documento
        fields = ['pdf', 'nome']
        read_only_fields = ['usuario']

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
