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
from .models import Post, Comentario
from django.utils import timezone
from .forms import PostForm, ContactForm
from django.core.mail import send_mail
from django.conf import settings
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            # Enviar correo (requiere configuración de correo en settings.py)
            send_mail(
                f"Mensaje de {nombre}",
                mensaje,
                correo,
                [settings.DEFAULT_FROM_EMAIL],
            )
            return redirect('contacto_exitoso')  # Redirige a una página de éxito
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})

def contacto_exitoso(request):
    return render(request, 'contacto_exitoso.html')

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

