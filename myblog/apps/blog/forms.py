from django import forms
from .models import Post, Comentario
        
class PostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ['titulo', 'autor', 'resumen', 'contenido', 'imagen', 'categorias', 'fecha_publicacion'] 
        widgets ={
            'titulo': forms.TextInput(attrs={'class':'textIntputClass'}),
            'contenido': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class FormPost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('autor', 'titulo', 'contenido')

        widgets ={
            'titulo': forms.TextInput(attrs={'class':'textIntputClass'}),
            'contenido': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class FormComentario(forms.Form):
    class Meta:
        model = Comentario
        fields = ('autor_comentario', 'cuerpo_comentario',)

        widgets ={
            'autor_comentario': forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
            'cuerpo_comentario': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent form-control', 'placeholder': 'Escribí aquí tu comentario!'}),
        }

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    correo = forms.EmailField(label="Correo")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")