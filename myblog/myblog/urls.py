"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from django.conf.urls.static import static
from django.conf import settings

from apps.blog.views import *
#from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.blog_auth.urls')),
    path("", index, name='index'),
    path('about/', about, name='about'),
    path('contacto/', contacto, name='contacto'),
    path('contacto/', contacto, name='contacto'),
    path('contacto-exitoso/', contacto_exitoso, name='contacto_exitoso'),  # Vista de éxito
    path("posts", lista_posts, name='lista_posts'),
    path("posts-detalle/<int:id>/", postdetalle, name='postdetalle'),
    path('post/<int:post_id>/comentario/', agregar_comentario, name='agregar_comentario'),
    path("actualizar-post/<int:id>/", actualizarpost, name='actualizarpost'),
    path("eliminar-post/<int:id>/", eliminarpost, name='eliminarpost'),
    re_path("post/nuevo", CreatePostView.as_view(), name='CreatePostView'),
    re_path('comentario/<int:id>/approve', aprobar_comentario, name='aprobar_comentario'),
    re_path('comentario/<int:id>/remove', eliminar_comentario, name='eliminar_comentario'),
    path("filtro-categorias/<categoria>/", lista_categorias, name='lista_categorias'),
    path('post/new/', create_post, name='create-post'),

    path('posts/alfabeticamente/', listar_posts_alfabeticamente, name='listar_posts_alfabeticamente'),
    path('posts/fechas/<str:tipo>/', fechas, name='listar_posts_fechas'),  # Captura el argumento "tipo"
    path('categoria/<int:categoria_id>/', listar_posts_por_categoria, name='listar_posts_por_categoria'),
    path('posts/alfabeticamente/<int:categoria_id>/', listar_posts_por_categoria, name='listar_posts_por_categoria'),
    path('categoria/<int:categoria_id>/', listar_posts_por_categoria, name='listar_posts_por_categoria'),
    path("inicio/", listar_posts, name="inicio2"),

   # path('', home_view, name= 'home_view'),
    #path('index', index, name= 'index'),
    #path('', indexview.as_view(), name='index'),
    #path('index', inicioview.as_view(), name='inicio')
] #path('contacto', Contacto, name='contacto'),
