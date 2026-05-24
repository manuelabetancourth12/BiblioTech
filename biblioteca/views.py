# biblioteca/views.py
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
from .models import Libro, Autor, Categoria, Prestamo
from .forms import LibroForm, AutorForm, CategoriaForm, RegistroPersonalizadoForm

# =========================================================================
# 1. CATÁLOGO PÚBLICO (Buscador integrado por Título, Autor o Categoría)
# =========================================================================
def lista_libros(request):
    libros = Libro.objects.all()
    buscar = request.GET.get('q')
    
    if buscar:
        libros = libros.filter(titulo__icontains=buscar) | \
                 libros.filter(autor__nombre__icontains=buscar) | \
                 libros.filter(categoria__nombre__icontains=buscar)
                 
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})


# =========================================================================
# 2. DASHBOARD PRINCIPAL (Métricas y datos para gráficos dinámicos)
# =========================================================================
@login_required
def dashboard(request):
    total_libros = Libro.objects.count()
    libros_prestados = Libro.objects.filter(estado='prestado').count()
    
    # Listas dinámicas para indicadores gráficos (Volumen por Categoría)
    categorias = Categoria.objects.all()
    cat_labels = [c.nombre for c in categorias]
    cat_valores = [Libro.objects.filter(categoria=c).count() for c in categorias]
    
    # Listas dinámicas para la Disponibilidad Física Total
    est_labels = ['Disponible', 'Prestado', 'Retrasado']
    est_valores = [
        Libro.objects.filter(estado='disponible').count(),
        Libro.objects.filter(estado='prestado').count(),
        Libro.objects.filter(estado='retrasado').count(),
    ]
    
    # Últimos 5 libros registrados para la cola de control operativo
    libros_lista = Libro.objects.all().order_by('-id')[:5]

    contexto = {
        'total_libros': total_libros,
        'libros_prestados': libros_prestados,
        'cat_labels': cat_labels,
        'cat_valores': cat_valores,
        'est_labels': est_labels,
        'est_valores': est_valores,
        'libros_lista': libros_lista,
    }
    return render(request, 'biblioteca/dashboard.html', contexto)


# =========================================================================
# 3. ACCIONES CRUD (Administración de Libros)
# =========================================================================
@login_required
def crear_libro(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Libro agregado exitosamente al catálogo!")
            return redirect('dashboard')
    else:
        form = LibroForm()
    return render(request, 'biblioteca/form_libro.html', {'form': form, 'accion': 'Agregar Nuevo'})

@login_required
def editar_libro(request, pk):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('dashboard')
        
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡El libro '{libro.titulo}' se actualizó correctamente!")
            return redirect('dashboard')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/form_libro.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_libro(request, pk):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('dashboard')
        
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, "El libro fue eliminado del catálogo permanente.")
    return redirect('dashboard')


# =========================================================================
# 4. CREACIÓN RÁPIDA (Autores y Categorías desde el Dashboard)
# =========================================================================
@login_required
def crear_autor(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso exclusivo para administradores.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Autor registrado exitosamente!")
            return redirect('dashboard')
    else:
        form = AutorForm()
    return render(request, 'biblioteca/form_libro.html', {'form': form, 'accion': 'Agregar Nuevo Autor'})

@login_required
def crear_categoria(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso exclusivo para administradores.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Categoría creada exitosamente!")
            return redirect('dashboard')
    else:
        form = CategoriaForm()
    return render(request, 'biblioteca/form_libro.html', {'form': form, 'accion': 'Agregar Nueva Categoría'})


# =========================================================================
# 5. MÓDULO TRANSACCIONAL (Reservas y Devoluciones de Libros)
# =========================================================================
@login_required
def reservar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    
    if libro.estado == 'disponible':
        ahora = timezone.now()
        devolucion_estimada = ahora + timedelta(days=7)
        
        prestamo = Prestamo(
            usuario=request.user,
            libro=libro,
            fecha_prestamo=ahora,
            fecha_devolucion_esperada=devolucion_estimada
        )
        prestamo.save()
        
        libro.estado = 'prestado'
        libro.save()
        
        messages.success(request, f"¡Has reservado '{libro.titulo}' con éxito! Revisa tus préstamos.")
    else:
        messages.error(request, "Lo sentimos, este libro ya no se encuentra disponible para reserva.")
        
    return redirect('lista_libros')

@login_required
def devolver_libro(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Acceso exclusivo para administradores y trabajadores.")
        return redirect('dashboard')
        
    libro = get_object_or_404(Libro, pk=pk)
    
    if libro.estado == 'prestado':
        libro.estado = 'disponible'
        libro.save()
        messages.success(request, f"¡El libro '{libro.titulo}' ha sido devuelto y está listo para estantería!")
    else:
        messages.error(request, "Este libro ya se encuentra disponible en el catálogo.")
        
    return redirect('dashboard')


# =========================================================================
# 6. REPORTES (Exportación a Excel / CSV)
# =========================================================================
@login_required
def exportar_libros_excel(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso exclusivo para administradores.")
        return redirect('dashboard')
        
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario_biblioteca.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Título del Libro', 'Autor', 'Categoría', 'Estado Actual'])
    
    libros = Libro.objects.all()
    for libro in libros:
        autor_nombre = libro.autor.nombre if libro.autor else 'No asignado'
        categoria_nombre = libro.categoria.nombre if libro.categoria else 'General'
        writer.writerow([libro.titulo, autor_nombre, categoria_nombre, libro.estado.upper()])
        
    return response


# =========================================================================
# 7. VISTAS OPERATIVAS COMPLEMENTARIAS Y AUTENTICACIÓN
# =========================================================================
@login_required
def lista_autores(request):
    autores = Autor.objects.all().order_by('nombre')
    return render(request, 'biblioteca/autores.html', {'autores': autores})

@login_required
def lista_prestamos(request):
    if request.user.is_staff:
        prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    else:
        prestamos = Prestamo.objects.filter(usuario=request.user).order_by('-fecha_prestamo')
    return render(request, 'biblioteca/prestamos.html', {'prestamos': prestamos})

@login_required
def lista_usuarios(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso exclusivo para administradores.")
        return redirect('dashboard')
    usuarios = User.objects.all().order_by('username')
    return render(request, 'biblioteca/usuarios.html', {'usuarios': usuarios})

@login_required
def lista_sanciones(request):
    return render(request, 'biblioteca/sanciones.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroPersonalizadoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            if form.cleaned_data['rol'] == 'staff':
                user.is_staff = True 
            user.save()
            messages.success(request, f'¡Cuenta de {user.username} creada con éxito! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroPersonalizadoForm()
    return render(request, 'autenticacion/registro.html', {'form': form})