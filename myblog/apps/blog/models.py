from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse

# Create your models here. posts
class Post (models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(null=True, blank=True, upload_to='img/posts', help_text='Seleccione una imágen para mostrar')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    categorias = models.ManyToManyField('Categoria', related_name='Post')

    def publicar(self):
        self.fecha_publicacion = timezone.now()
        self.save()
    
    def __str__(self):
        return self.titulo
    
    def mostrarComentarios(self):
        return self.comentario.filter(aprobado=True)
    
    def get_absolute_url(self):
        #return reverse('apps.blog:blog_detail', args=(str(self.id)))
        return reverse("apps.blog:blog_detalle",kwargs={'id':self.id})


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comentario (models.Model):
    post = models.ForeignKey('Post', related_name='Comentarios', on_delete=models.CASCADE)
    autor_comentario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuerpo_comentario = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=True)

    def aprobarComentario(self):
        self.aprobado=True
        self.save()

    def eliminar(self):
        self.aprobado=False
        self.save()
