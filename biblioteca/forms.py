from django import forms
from .models import Libro
from django.contrib.auth.models import User

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'categoria', 'estado', 'imagen_portada']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos de diseño pastel directamente a cada input del formulario
        clase_comun = "w-full px-4 py-2.5 rounded-xl border border-pink-100 bg-white text-sm text-slate-700 focus:outline-none focus:border-pink-300 transition"
        
        for field_name, field in self.fields.items():
            if field_name != 'imagen_portada':
                field.widget.attrs.update({'class': clase_comun})
            else:
                field.widget.attrs.update({'class': "text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-pink-50 file:text-pink-600 hover:file:bg-pink-100 cursor-pointer"})

from .models import Autor, Categoria

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clase_comun = "w-full px-4 py-2.5 rounded-xl border border-pink-100 bg-white text-sm text-slate-700 focus:outline-none focus:border-pink-300 transition"
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': clase_comun})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clase_comun = "w-full px-4 py-2.5 rounded-xl border border-pink-100 bg-white text-sm text-slate-700 focus:outline-none focus:border-pink-300 transition"
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': clase_comun})

# biblioteca/forms.py (Añadir al final)
from django.contrib.auth.models import User

class RegistroPersonalizadoForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    
    TIPO_USUARIO = [
        ('lector', 'Lector (Explorar catálogo)'),
        ('staff', 'Bibliotecario (Administrar todo)')
    ]
    rol = forms.ChoiceField(choices=TIPO_USUARIO, label="Tipo de Cuenta", widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clase_input = "w-full px-4 py-2.5 rounded-xl border border-pink-100 bg-white text-sm text-slate-700 focus:outline-none focus:border-pink-300 transition mb-4"
        self.fields['username'].widget.attrs.update({'class': clase_input, 'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update({'class': clase_input, 'placeholder': 'Crea una contraseña'})
        self.fields['password_confirm'].widget.attrs.update({'class': clase_input, 'placeholder': 'Repite la contraseña'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data