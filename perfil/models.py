from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuario')
    nome = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    pais = models.CharField(max_length=40)
    foto = models.ImageField(upload_to='user_foto/%Y/%m/%d')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
