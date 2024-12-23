from django.contrib import admin
from .models import Post, Categoria, Comentario
from django.utils.safestring import mark_safe

# Register your models here.
class CategoriasInline(admin.StackedInline):
    model = Post.categorias.through
    extra=5

class PostAdmin(admin.ModelAdmin):
    model=Post
    inlines=(CategoriasInline,)
    #exclude=('categorias',)
    raw_id_fields=('categorias',)
    list_display=('titulo', 'autor', 'imagen', 'categoria',)
    search_fields= ('titulo', 'autor', 'fecha_creacion',)
    list_per_page = 25

    readonly_fields = ['noticia_img',]

    def categoria(self, obj):
        return "\n".join([c.nombre for c in obj.categorias.all()])

    def noticia_img(self, obj):
        if obj.imagen:  # Verificamos si hay una imagen antes de renderizar
            return mark_safe(
                f'<a href="{obj.imagen.url}"><img src="{obj.imagen.url}" width="10%"/></a>'
            )
        return "No image available"
    #def noticia_img(self, obj):
    #    return mark_safe('<a href=¨{0}¨ width=¨30%¨/></a>'.format(self.imagen.url))

    fieldsets =(
        ('contenido del post', {'description':'ingrese la informacion de titulo y contenido de la noticia', 
        'fields':[('titulo','autor'), 'contenido', 'noticia_img', 'fecha_creacion', 'fecha_publicacion']}
    ),)

class ComentariosAdmin(admin.ModelAdmin):
    list_display=('autor_comentario', 'cuerpo_comentario', 'post', 'fecha_creacion', 'aprobado')
    list_filter=('aprobado', 'fecha_creacion')
    search_fields = ('autor_comentario', 'cuerpo_comentario')
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)

admin.site.register(Categoria, admin.ModelAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentariosAdmin)

