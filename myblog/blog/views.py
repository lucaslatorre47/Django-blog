from django.shortcuts import render
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from .models import Post
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

