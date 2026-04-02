# Sistema de Gestión de Biblioteca con Django

Aplicación web desarrollada en Python con Django para la gestión de libros, usuarios y préstamos, implementando operaciones CRUD y control de disponibilidad de ejemplares.

## Características

- Registro, edición, consulta y eliminación de libros
- Registro, edición, consulta y eliminación de usuarios
- Gestión de préstamos y devoluciones
- Control automático de disponibilidad de libros
- Validación para evitar préstamos duplicados de un mismo libro
- Interfaz web con plantillas HTML y Bootstrap

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- Bootstrap

## Estructura general

- `core/`: lógica principal de la aplicación
- `templates/`: vistas HTML del sistema
- `config/`: configuración general del proyecto Django
- `manage.py`: administrador del proyecto

## Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/sistema-biblioteca-django.git