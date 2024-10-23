from django.shortcuts import render
fron django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import FormView
from forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoguinRequiredMixin

# Create your views here.
class SignUpView(FormView):
    template_name = 'auth/registro.html'
    form_class = SignUpForm
    succes_url = reverse_lazy('apps.blog_auth:login')

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

'''class Login(auth_views.LoginView):
    template_name = 'auth/login.html' '''


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('apps.blog_auth:login')
        else:
            messages.error(request, 'credenciales incorrectas')
    return render(render, 'auth/login.html')

class Logout(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'auth/logout.html'
    