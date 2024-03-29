# Generated by Django 3.2.19 on 2024-02-04 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0028_delete_funcionarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre1', models.CharField(default='', max_length=50, verbose_name='Primer nombre')),
                ('nombre2', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Segundo nombre')),
                ('apellido1', models.CharField(default='', max_length=50, verbose_name='Primer apellido')),
                ('apellido2', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Segundo apellido')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('foto', models.FileField(default='', upload_to='fotos/', verbose_name='Archivo con Foto del Funcionario (200 x 200px)')),
                ('direccion', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Dirección Residencia')),
                ('celular', models.CharField(blank=True, default='', max_length=60, null=True, verbose_name='Número de celular')),
                ('email', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='E-Mail')),
                ('tipo_contrato', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de labores')),
                ('cargo', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='generales.cargos')),
                ('sede', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='generales.sedes')),
            ],
        ),
    ]
