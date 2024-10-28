from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import Http404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin  #from django.contrib import messages
from django.views.generic import(CreateView)
from django.contrib.auth.decorators import login_required
from apps.blog.forms import FormComentario, FormPost
from django.contrib import messages
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from .models import Post, Comentario, Categoria
from django.utils import timezone
from .forms import PostForm
# Create your views here.

def index(request):
    ultimos_posts= Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request,'index.html',{'ultimos_posts':ultimos_posts})

def about(request):
    return render(request, 'about.html')

def lista_posts(request):
   # posts = Post.objects.filter(fecha_publicacion=timezone.now()).order_by('fecha_publicacion')
    posts= Post.objects.all().order_by('fecha_publicacion')
    #ultimos_posts= Post.objects.all().order_by('fecha_publicacion').reverse()[:3] por si queremos mostrar los últimos 3 posts
    return render(request,'posts.html',{'posts':posts})

def lista_categorias(request, categoria):
    posts = Post.objects.filter(
        categories__name__contains=categoria
    ).order_by("-fecha_creacion")
    context = {
        "categoria": categoria,
        "posts": posts,
        
    }
    return render(request, "blog/lista_categorias.html", context) 

class CreatePostView(CreateView, LoginRequiredMixin):
    login_url= '/login'
    #redirect_field_name='createpost.html'

    form_class = FormPost

    model = Post

def postdetalle(request,id):
    try:
        data = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(aprobado=True)
        form = FormComentario()
        if request.method == "POST":
            form = FormComentario(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = data
                comentario.save()
                return redirect('post_detalle', id=data.id)
    except Post.DoesNotExist:
        raise Http404('El Post seleccionado no existe.')
    
    comentarios = Comentario.objects.all()
    context={
        "post": data,
        "comentarios": comentarios,
        "form": FormComentario()
    }
    return render(request, 'post_detalle.html', context)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo post en la base de datos
            return redirect('index')  # Redirige a la página de inicio después de guardar
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

def contacto(request):
    return render(request, 'contacto.html')

def listar_posts_por_categoria(request, categoria_id):
    global categoria,categorias
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)  # Filtra los posts por la categoría seleccionada
    categorias = Categoria.objects.all()  # Obtén todas las categorías para el aside


    return render(request, 'filtrado_categorias.html', {
        'posts': posts,
        'categorias': categorias,  # Pasa las categorías para el aside
        'mostrar_categorias': True,
        'mostrar_fechas': True,
        'mostrar_cargas': True
    })

def listar_posts_alfabeticamente(request):

    categorias = Categoria.objects.all()  # Asegúrate de obtener las categorías


    orden = request.GET.get('orden', 'asc')  # Obtener el parámetro de orden de la URL
    if orden == 'desc':
        ultimosposts = Post.objects.all().order_by('-titulo')[:4]  # Ordenar de Z a A
    else:
        ultimosposts = Post.objects.all().order_by('titulo')[:4]  # Ordenar de A a Z

    return render(request, 'inicio.html', {'ultimosposts': ultimosposts, 
                                           'mostrar_cargas': True,
                                           'categorias': categorias, 
                                           'mostrar_fechas': True,
                                           'mostrar_categorias': True})


def fechas(request, tipo):
    categorias = Categoria.objects.all()  # Asegúrate de obtener las categorías
    if tipo == 'recientes':
        ultimosposts = Post.objects.all().order_by('-fecha_publicacion')[:4]  # Más recientes
    elif tipo == 'antiguos':
        ultimosposts = Post.objects.all().order_by('fecha_publicacion')[:4]  # Más antiguos
    else:
        ultimosposts = Post.objects.all()  # O una lista vacía, según lo que desees
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts,
                                           'categorias': categorias, 
                                           'mostrar_cargas': True, 
                                           'mostrar_fechas': True,
                                           'mostrar_categorias': True})

def listar_posts(request):
    posts = Post.objects.all()  # Obtén todos los posts
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    ultimosposts = Post.objects.all().order_by('fecha_publicacion')  # Cambia si necesitas limitar e numero de post
    #ultimos_mensajes = MensajeContacto.objects.order_by('-fecha_envio')[:3]
    ## implementacion

    # Filtrar posts si hay un parámetro de categoría en la URL
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categorias__id=categoria_id)

    return render(request, 'inicio2.html', 
                  {'ultimosposts': ultimosposts, 
                   'categorias': categorias ,
                   'mostrar_categorias': True,
                   'mostrar_fechas': True,
                   #'ultimos_mensajes': ultimos_mensajes
                   })


def listar_categorias(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    posts = Post.objects.all()  # Puedes agregar esto si deseas también listar los posts
    return render(request, 'base.html', {'categorias': categorias,
                                           'posts': posts,
                                           'mostrar_cargas': True,
                                           'mostrar_fechas': True})


@login_required
def actualizarpost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse('Post no encontrado', status=404)
    
    if request.method == 'POST':
        form = FormPost(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actualizarpost', id=post.id)
    else:
        FormPost(instance=post)

    return render(request, 'actualizarpost.html', )#{'form': form, 'post': post})   


@login_required
def eliminarpost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse('Post no encontrado', status=404)
    
    if request.method == 'POST':
        post.delete()
        return redirect('lista_posts')

    return render(request, 'postdelete.html', )#{'form': form, 'post': post})    


@login_required
def publicar_post(request, id):
    try:
        post =Post.objects.get(id =id)
    except Post.DoesNotExist:
        raise Http404('No existe el post seleccionado')
    post.publicar()
    return redirect('post_detail', id=id)

#@login_required
def agregar_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST': #and request.user.is_authenticated:
        contenido = request.POST.get('contenido')

        if contenido:  # Verificamos que el contenido no esté vacío
            Comentario.objects.create(
                autor_comentario=request.user,
                post=post,
                cuerpo_comentario=contenido
            )
            messages.success(request, '¡Comentario agregado con éxito!')  # Mensaje de éxito
        else:
            messages.error(request, 'No puedes enviar un comentario vacío.')  # Manejo de error

        return redirect('postdetalle', id=post_id)  # Redirige de nuevo a la página del post

    return redirect('postdetalle', id=post_id)  # Redirige si no es un POST válido


@login_required
def aprobar_comentario(request, id):
    try:
        comment =Comentario.objects.get(id =id)
    except Comentario.DoesNotExist:
        raise Http404('Comentario no existe')
    comment.aprobarComentario()
    return redirect('post_detalle', id=comment.post.id)


@login_required
def eliminar_comentario(request, id):
    try:
        comment =Comentario.objects.get(id =id)
    except Comentario.DoesNotExist:
        raise Http404('No existe Comentario')
    post_id = comment.post.id
    comment.eliminarComentario()
    return redirect('post_detalle', id=post_id)




'''
def home_view(request):
    return HttpResponse('Esto es una página de prueba')

def index (request):
    return render (request, 'inicio.html')

class indexview (View):
    def get(self, request):
        return HttpResponse('Esta es la página Principal')

class inicioview(TemplateView):
    template_name = 'inicio.html'
'''

