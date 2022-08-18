from django.contrib import admin
from .models import Sedes, Profile, Cargos, Funcionarios, Noticias, Suscribir, Miempresa, Bienestar, Ocupacional, Reglamento
from django.contrib.admin.widgets import AutocompleteSelect

class SedesAdmin(admin.ModelAdmin):
    list_display = ('nombre_sede','foto','director','ciudad', )
    ordering = ('nombre_sede', )

    class Meta:
        model = Sedes

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'foto', 'sede',)
    ordering = ['user',]
    search_fields = ('user', )

    class Meta:
        model = Profile


class CargosAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    ordering = ['nombre']
    search_fields = ('nombre', )

    class Meta:
        model = Cargos


class FuncionariosAdmin(admin.ModelAdmin):
    list_display = ('nombre1','nombre2','apellido1','apellido2','foto','sede','direccion','cargo','celular','email',)
    ordering = ['sede','apellido1','nombre1',]
    search_fields = ('nombre1','nombre2','apellido1','apellido2',)
    list_filter = ('sede',)

    class Meta:
        model = Funcionarios


class NoticiasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'sede', 'ultima_hora', 'orden_destacado', 'imagen_destacado', 'modificado','activo', )
    fields = ['titulo', 'subtitulo', 'sede', 'evento', ('orden_destacado', 'imagen_destacado'), 'descripcion', 'archivo_audio', 'urlvideo', 'ultima_hora', 'fuente', 'html', 'pdf', 'activo', ('fecha_inicio_publicacion', 'fecha_final_publicacion')]
    exclude = ('slug','autor', 'modificado',)
    ordering = ('sede', 'orden_destacado', 'titulo', '-modificado')
    search_fields = ('titulo','subtitulo','sede')
    list_filter = ('modificado', 'sede', 'orden_destacado')

    class Meta:
        model = Noticias

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


class MiempresaAdmin(admin.ModelAdmin):
    list_display = ('nuestra_empresa', 'mision', 'vision', 'objetivo', 'principios', 'himno_letra', 'himno_audio', )
    fields = ['nuestra_empresa', 'mision', 'vision', 'objetivo', 'principios', 'himno_letra', 'himno_audio',]

    class Meta:
        model = Miempresa

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Miempresa, MiempresaAdmin)
admin.site.register(Sedes, SedesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cargos, CargosAdmin)
admin.site.register(Funcionarios, FuncionariosAdmin)
admin.site.register(Noticias, NoticiasAdmin)
admin.site.register(Bienestar)
admin.site.register(Ocupacional)
admin.site.register(Reglamento)
