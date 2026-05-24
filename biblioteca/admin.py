# biblioteca/admin.py
from django.contrib import admin
from .models import Categoria, Autor, Libro, Prestamo

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'categoria', 'estado')
    list_filter = ('estado', 'categoria')
    search_fields = ('titulo', 'autor__nombre')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion_esperada', 'fecha_devolucion_real')
    list_filter = ('fecha_prestamo', 'libro__estado')