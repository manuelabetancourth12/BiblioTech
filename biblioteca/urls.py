# biblioteca/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Catálogo y Dashboard Principales
    path('', views.lista_libros, name='lista_libros'),
    path('dashboard/exportar/', views.exportar_libros_excel, name='exportar_libros_excel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 2. CRUD de Administración para Libros
    path('libro/nuevo/', views.crear_libro, name='crear_libro'),
    path('libro/editar/<int:pk>/', views.editar_libro, name='editar_libro'),
    path('libro/eliminar/<int:pk>/', views.eliminar_libro, name='eliminar_libro'),
    
    # biblioteca/urls.py (Añadir dentro de urlpatterns)
    path('libro/devolver/<int:pk>/', views.devolver_libro, name='devolver_libro'),

    # 3. Accesos Rápidos para Configurar el Catálogo
    path('autor/nuevo/', views.crear_autor, name='crear_autor'),
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    
    # 4. Acción Interactiva de Reserva
    path('libro/reservar/<int:pk>/', views.reservar_libro, name='reservar_libro'),
    
    # 5. Otras Secciones Operativas
    path('autores/', views.lista_autores, name='lista_autores'),
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('sanciones/', views.lista_sanciones, name='lista_sanciones'),
    
    # 6. Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='autenticacion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_libros'), name='logout'),
]