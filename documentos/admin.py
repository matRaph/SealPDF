from django.contrib import admin

# Register your models here.

from .models import Documento, Permissao

admin.site.register(Documento)
admin.site.register(Permissao)
