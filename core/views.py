from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Usuario, Prestamo


def sincronizar_disponibilidad_libros():
    for libro in Libro.objects.all():
        tiene_prestamo_activo = Prestamo.objects.filter(
            libro=libro,
            devuelto=False
        ).exists()
        libro.disponible = not tiene_prestamo_activo
        libro.save(update_fields=["disponible"])


# =========================
# INICIO
# =========================
def inicio(request):
    sincronizar_disponibilidad_libros()

    contexto = {
        "total_libros": Libro.objects.count(),
        "libros_disponibles": Libro.objects.filter(disponible=True).count(),
        "libros_prestados": Libro.objects.filter(disponible=False).count(),
        "total_usuarios": Usuario.objects.count(),
        "total_prestamos": Prestamo.objects.count(),
        "prestamos_activos": Prestamo.objects.filter(devuelto=False).count(),
    }
    return render(request, "inicio.html", contexto)


# =========================
# LIBROS
# =========================
def lista_libros(request):
    sincronizar_disponibilidad_libros()

    busqueda = request.GET.get("busqueda", "").strip()
    libros = Libro.objects.all()

    if busqueda:
        libros = libros.filter(
            Q(titulo__icontains=busqueda) |
            Q(autor__icontains=busqueda) |
            Q(isbn__icontains=busqueda)
        )

    return render(request, "libros/lista.html", {
        "libros": libros,
        "busqueda": busqueda
    })


def crear_libro(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        autor = request.POST.get("autor", "").strip()
        isbn = request.POST.get("isbn", "").strip()
        editorial = request.POST.get("editorial", "").strip()
        anio_publicacion = request.POST.get("anio_publicacion", "").strip()

        if not titulo or not autor or not isbn or not anio_publicacion:
            messages.error(request, "Debes completar todos los campos obligatorios.")
            return render(request, "libros/crear.html")

        if Libro.objects.filter(isbn=isbn).exists():
            messages.error(request, "Ya existe un libro con ese ISBN.")
            return render(request, "libros/crear.html")

        Libro.objects.create(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            editorial=editorial,
            anio_publicacion=anio_publicacion,
            disponible=True
        )
        messages.success(request, "Libro creado correctamente.")
        return redirect("lista_libros")

    return render(request, "libros/crear.html")


def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        autor = request.POST.get("autor", "").strip()
        isbn = request.POST.get("isbn", "").strip()
        editorial = request.POST.get("editorial", "").strip()
        anio_publicacion = request.POST.get("anio_publicacion", "").strip()

        if not titulo or not autor or not isbn or not anio_publicacion:
            messages.error(request, "Debes completar todos los campos obligatorios.")
            return render(request, "libros/editar.html", {"libro": libro})

        if Libro.objects.filter(isbn=isbn).exclude(id=libro.id).exists():
            messages.error(request, "Ya existe otro libro con ese ISBN.")
            return render(request, "libros/editar.html", {"libro": libro})

        libro.titulo = titulo
        libro.autor = autor
        libro.isbn = isbn
        libro.editorial = editorial
        libro.anio_publicacion = anio_publicacion
        libro.disponible = not Prestamo.objects.filter(libro=libro, devuelto=False).exists()
        libro.save()

        messages.success(request, "Libro actualizado correctamente.")
        return redirect("lista_libros")

    return render(request, "libros/editar.html", {"libro": libro})


def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if Prestamo.objects.filter(libro=libro, devuelto=False).exists():
        messages.error(request, "No se puede eliminar el libro porque tiene un préstamo activo.")
        return redirect("lista_libros")

    libro.delete()
    messages.success(request, "Libro eliminado correctamente.")
    return redirect("lista_libros")


# =========================
# USUARIOS
# =========================
def lista_usuarios(request):
    busqueda = request.GET.get("busqueda", "").strip()
    usuarios = Usuario.objects.all()

    if busqueda:
        usuarios = usuarios.filter(
            Q(nombre__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )

    return render(request, "usuarios/lista.html", {
        "usuarios": usuarios,
        "busqueda": busqueda
    })


def crear_usuario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        if not nombre or not correo:
            messages.error(request, "Nombre y correo son obligatorios.")
            return render(request, "usuarios/crear.html")

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, "usuarios/crear.html")

        Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )
        messages.success(request, "Usuario creado correctamente.")
        return redirect("lista_usuarios")

    return render(request, "usuarios/crear.html")


def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        if not nombre or not correo:
            messages.error(request, "Nombre y correo son obligatorios.")
            return render(request, "usuarios/editar.html", {"usuario": usuario})

        if Usuario.objects.filter(correo=correo).exclude(id=usuario.id).exists():
            messages.error(request, "Ya existe otro usuario con ese correo.")
            return render(request, "usuarios/editar.html", {"usuario": usuario})

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.telefono = telefono
        usuario.save()

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("lista_usuarios")

    return render(request, "usuarios/editar.html", {"usuario": usuario})


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if Prestamo.objects.filter(usuario=usuario, devuelto=False).exists():
        messages.error(request, "No se puede eliminar el usuario porque tiene préstamos activos.")
        return redirect("lista_usuarios")

    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("lista_usuarios")


# =========================
# PRESTAMOS
# =========================
def lista_prestamos(request):
    sincronizar_disponibilidad_libros()
    prestamos = Prestamo.objects.select_related("usuario", "libro").all()
    return render(request, "prestamos/lista.html", {"prestamos": prestamos})


def crear_prestamo(request):
    sincronizar_disponibilidad_libros()

    usuarios = Usuario.objects.all()
    libros = Libro.objects.filter(disponible=True)

    if request.method == "POST":
        usuario_id = request.POST.get("usuario_id")
        libro_id = request.POST.get("libro_id")

        if not usuario_id or not libro_id:
            messages.error(request, "Debes seleccionar un usuario y un libro.")
            return render(request, "prestamos/crear.html", {
                "usuarios": usuarios,
                "libros": libros
            })

        usuario = get_object_or_404(Usuario, id=usuario_id)
        libro = get_object_or_404(Libro, id=libro_id)

        if Prestamo.objects.filter(libro=libro, devuelto=False).exists():
            libro.disponible = False
            libro.save(update_fields=["disponible"])
            messages.error(request, "Ese libro ya tiene un préstamo activo.")
            return render(request, "prestamos/crear.html", {
                "usuarios": usuarios,
                "libros": Libro.objects.filter(disponible=True)
            })

        Prestamo.objects.create(
            usuario=usuario,
            libro=libro,
            devuelto=False
        )

        libro.disponible = False
        libro.save(update_fields=["disponible"])

        messages.success(request, "Préstamo registrado correctamente.")
        return redirect("lista_prestamos")

    return render(request, "prestamos/crear.html", {
        "usuarios": usuarios,
        "libros": libros
    })


def devolver_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if prestamo.devuelto:
        messages.warning(request, "Ese préstamo ya fue devuelto.")
        return redirect("lista_prestamos")

    if request.method == "POST":
        fecha_devolucion = request.POST.get("fecha_devolucion")
        prestamo.devuelto = True
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.save()

        tiene_otro_activo = Prestamo.objects.filter(
            libro=prestamo.libro,
            devuelto=False
        ).exists()

        prestamo.libro.disponible = not tiene_otro_activo
        prestamo.libro.save(update_fields=["disponible"])

        messages.success(request, "Libro devuelto correctamente.")
        return redirect("lista_prestamos")

    return redirect("lista_prestamos")