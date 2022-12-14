
from django import forms
from datetime import date
from django.forms.models import inlineformset_factory

from genteinrai.settings import CKEDITOR_CONFIGS
from .models import Suscribir, Elmuro
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
from django.conf import settings

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


class ComentarioForm(forms.ModelForm):
    foto = forms.FileField()
    detalle=forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Elmuro
        fields = ('titulo', 'detalle', 'foto')
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['foto'].required = False
        
    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"]
        if not titulo:
            raise forms.ValidationError("Titulo Requerido")
        return titulo

    def clean_detalle(self):
        detalle = self.cleaned_data["detalle"]
        if not detalle:
            raise forms.ValidationError("Comentario Requerido")
        return detalle

    def clean_foto(self):
        foto = self.cleaned_data["foto"]
        return foto


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


