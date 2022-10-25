from django.db import models
from novel.models import Novel
from django.contrib.auth.models import User
from django.utils import timezone


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=50)
    email_comentario = models.EmailField()
    comentario = models.TextField()
    novel_comentario = models.ForeignKey(Novel, on_delete=models.CASCADE)
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_comentario = models.DateTimeField(default=timezone.now)
    publicado_comentario = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_comentario
