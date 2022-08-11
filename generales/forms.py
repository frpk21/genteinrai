
from django import forms
from datetime import date
from django.forms.models import inlineformset_factory
from .models import Suscribir, Noticias
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from ckeditor.widgets import CKEditorWidget

class SuscribirseForm(forms.ModelForm):
    
    class Meta:
        model = Suscribir
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError("Email Requerido")
        return email

hoy = date.today()
mes_actual = hoy.month
CHOICES = [
    (1,'ENERO'),
    (2,'FEBRERO'),
    (3,'MARZO'),
    (4,'ABRIL'),
    (5,'MAYO'),
    (6,'JUNIO'),
    (7,'JULIO'),
    (8,'AGOSTO'),
    (9,'SEPTIEMBRE'),
    (10,'OCTUBRE'),
    (11,'NOVIEMBRE'),
    (12,'DICIEMBRE')
    ]

class MesAnoForm(forms.Form):
    mes_consulta = forms.DateField(widget=forms.SelectDateWidget(months=CHOICES))


