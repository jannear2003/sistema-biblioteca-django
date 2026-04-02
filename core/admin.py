from django.contrib import admin
from .models import Usuario, Libro, Prestamo


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'correo')
    list_per_page = 10


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'anio_publicacion', 'disponible')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('disponible',)
    list_per_page = 10


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'devuelto')
    search_fields = ('usuario__nombre', 'libro__titulo')
    list_filter = ('devuelto', 'fecha_prestamo')
    list_per_page = 10