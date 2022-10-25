from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Novel, Volume, Capitulo


class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 1


class CapituloInline(admin.TabularInline):
    model = Capitulo
    extra = 1


class NovelAdmin(SummernoteModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'data', 'categoria', 'publicado')
    list_editable = ('publicado',)
    list_display_links = ('id', 'titulo')
    summernote_fields = ('excerto',)
    inlines = [
        VolumeInline
    ]


class VolumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'vol_vol', 'novel_vol',)
    list_display_links = ('id', 'vol_vol')
    inlines = [
        CapituloInline
    ]


class CapituloAdmin(SummernoteModelAdmin):
    list_display = ('id', 'numero_cap', 'volume_cap', 'titulo_cap')
    list_display_links = ('id', 'numero_cap', 'volume_cap', 'titulo_cap')
    summernote_fields = ('conteudo_cap',)


admin.site.register(Novel, NovelAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Capitulo, CapituloAdmin)
