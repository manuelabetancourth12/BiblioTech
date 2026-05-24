# 📚 BiblioTech - Sistema de Gestión de Biblioteca Universitaria

BiblioTech es una aplicación web responsiva e interactiva desarrollada en **Django** y estilizada con **Tailwind CSS**. El sistema está diseñado bajo una arquitectura de roles diferenciados, permitiendo a los estudiantes (Lectores) reservar libros en tiempo real, mientras que el personal administrativo (Bibliotecarios) gestiona el inventario, registra devoluciones y exporta reportes operativos.

---

## 🛠️ Requisitos Técnicos del Taller Cumplidos

1. **Autenticación y Autorización Avanzada (RBAC):** Sistema de inicio de sesión, cierre de sesión y registro con validación de credenciales. Soporte nativo para dos roles: *Lector* y *Bibliotecario (Staff)* mediante el uso de decoradores `@login_required` y verificación de privilegios.
2. **Modelado de Datos Relacional:** Estructura de base de datos compuesta por 4 modelos principales interconectados mediante llaves foráneas (`ForeignKey`): `Libro`, `Autor`, `Categoria` y `Prestamo`.
3. **Operaciones CRUD Completas:** Panel operativo exclusivo para el administrador que permite Crear, Consultar, Actualizar y Eliminar registros del catálogo mediante formularios controlados (`ModelForms`).
4. **Dashboard Estadístico e Indicadores:** Panel de control con métricas clave y dos gráficos dinámicos integrados basados en componentes nativos de Tailwind y JavaScript que procesan los datos en tiempo real.
5. **Reportes y Exportación:** Función de extracción de datos relacionales a un archivo descargable en formato compatible con Microsoft Excel (.CSV) con un solo clic.
6. **Interfaz de Usuario Limpia y Responsiva:** Maquetación moderna basada en una paleta de colores pasteles (blanco y acentos rosa/azul), equipada con barra lateral de navegación, menús fluidos y alertas de confirmación dinámicas.

---

## 📐 Arquitectura de Modelos (Base de Datos)

* **Categoria:** Almacena los géneros literarios para la segmentación del inventario.
* **Autor:** Registra el directorio oficial de escritores.
* **Libro:** Modelo central que almacena el título, portada, relación al autor/categoría y su estado de disponibilidad física (`disponible`, `prestado`, `retrasado`).
* **Prestamo:** Modelo transaccional que conecta un `User` con un `Libro`, registrando de forma estricta la `fecha_prestamo` y calculando la `fecha_devolucion_esperada`.

---

## 🗺️ Enrutamiento y Rutas Principales (`urls.py`)

### 🔓 Acceso Público y Clientes
* `GET /` : Catálogo general de libros con buscador en tiempo real.
* `POST /libro/reservar/<id>/` : Acción interactiva para que un Lector reserve un ejemplar disponible (calcula +7 días de límite).

### 🔒 Acceso Exclusivo de Administración (Staff)
* `GET /dashboard/` : Panel de control, métricas de inventario y gráficos dinámicos.
* `GET /dashboard/exportar/` : Descarga instantánea del reporte de inventario en Excel.
* `POST /libro/nuevo/` | `/libro/editar/<id>/` | `/libro/eliminar/<id>/` : Gestión CRUD del catálogo.
* `POST /libro/devolver/<id>/` : Libera un libro prestado y lo vuelve a poner disponible.
* `GET /autor/nuevo/` | `/categoria/nueva/` : Formularios de creación rápida.

---

## 🚀 Instrucciones de Instalación y Despliegue Local

Sigue estos comandos en tu terminal de Windows para inicializar el proyecto desde cero:

1. **Clonar o descargar el repositorio:**
   ```cmd
   git clone [https://github.com/manuelabetancourth12/BiblioTech.git](https://github.com/manuelabetancourth12/BiblioTech.git)
   cd BiblioTech