from django.db import models
from django.contrib.auth.models import User
import hashlib

class Documento(models.Model):
    pdf = models.FileField(upload_to='pdfs/')
    nome = models.CharField(max_length=255)
    hash = models.CharField(max_length=64, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)

            if self.pdf and not self.hash:
                with self.pdf.open('rb') as file:
                    bytes = file.read()
                    self.hash = hashlib.sha256(bytes).hexdigest()

                super().save(update_fields=['hash'])

    def check_hash(self):
        with self.pdf.open('rb') as file:
            bytes = file.read()  # Read the entire file
            conteudo_hash = hashlib.sha256(bytes).hexdigest()

        return conteudo_hash == self.hash
    
    def __str__(self):
        return self.nome
    

class Permissao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    permissao = models.CharField(max_length=1, choices=[('R', 'Leitura'), ('W', 'Escrita'), ('C','Verificação')])

    def __str__(self):
        return f'{self.usuario} - {self.permissao}'