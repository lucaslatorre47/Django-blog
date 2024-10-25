from django.shortcuts import render, redirect
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(CreateView)
from django.contrib.auth.decorators import login_required
from apps.blog.forms import FormComentario, FormPost
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from .models import Post, Comentario
from django.utils import timezone
# Create your views here.
def index(request):
    ultimos_posts= Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request,'index.html',{'ultimos_posts':ultimos_posts})



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


def Contacto(request):
    return render(request, 'contacto.html')


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

