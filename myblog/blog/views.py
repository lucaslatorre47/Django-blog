from django.shortcuts import render
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from .models import Post
from django.utils import timezone
# Create your views here.
def lista_posts(request):
    posts = Post.objects.filter(fecha_publicacion=timezone.now()).order_by('fecha_publicacion')
    return render(request,'posts.html',{'posts':posts})


#posts


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

