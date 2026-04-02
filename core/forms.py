from django import forms
from .models import Libro, Usuario, Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["usuario", "libro"]
        widgets = {
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "libro": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].queryset = Usuario.objects.all()
        self.fields["libro"].queryset = Libro.objects.filter(disponible=True)
        self.fields["usuario"].empty_label = "Seleccione un usuario"
        self.fields["libro"].empty_label = "Seleccione un libro"

    def clean_libro(self):
        libro = self.cleaned_data["libro"]
        if Prestamo.objects.filter(libro=libro, devuelto=False).exists():
            raise forms.ValidationError("Ese libro ya tiene un préstamo activo.")
        return libro