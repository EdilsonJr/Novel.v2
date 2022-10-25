from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Novel, Volume, Capitulo
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario


class NovelIndex(ListView):
    model = Novel
    template_name = 'novel/index.html'
    context_object_name = 'novels'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('id').filter(publicado=True)
        qs = qs.annotate(
            qtd_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return qs


class NovelBusca(NovelIndex):
    template_name = 'novel/novel_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()

        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo__icontains=termo) |
            Q(excerto__icontains=termo) |
            Q(categoria__nome_cat__iexact=termo) |
            Q(autor__username__iexact=termo)
        )

        return qs


class NovelCategoria(NovelIndex):
    template_name = 'novel/novel_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria__nome_cat__iexact=categoria)

        return qs


class NovelDetalhes(UpdateView):
    template_name = 'novel/novel_detalhes.html'
    model = Novel
    form_class = FormComentario
    context_object_name = 'novel'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        novel = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario=True,
                                                novel_comentario=novel.id)
        contexto['comentarios'] = comentarios
        return contexto

    def form_valid(self, form):
        novel = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.novel_comentario = novel

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        return redirect('novel_detalhes', pk=novel.id)


class VolumeDetalhes(UpdateView):
    template_name = 'novel/volume_detalhes.html'
    model = Volume
    form_class = FormComentario
    context_object_name = 'volume'
    slug_url_kwarg = 'slug_vol'
    slug_field = 'slug_vol'


class CapituloDetalhes(UpdateView):
    template_name = 'novel/capitulo_detalhes.html'
    model = Capitulo
    form_class = FormComentario
    context_object_name = 'capitulo'
    slug_url_kwarg = 'slug_cap'
    slug_field = 'slug_cap'
