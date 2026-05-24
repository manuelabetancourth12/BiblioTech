# biblioteca/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    ESTADOS = (
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('retrasado', 'Retrasado'),
    )
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)  # Relación 1
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relación 2
    imagen_portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')  # Requisito func. 4

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)  # Relación 3
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación 4 (Lector/Bibliotecario)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    sancion_aplicada = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Requisito func. 9

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"