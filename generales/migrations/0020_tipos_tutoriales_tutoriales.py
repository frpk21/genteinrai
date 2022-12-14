# Generated by Django 2.2.1 on 2022-08-25 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0019_elmuro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipos_tutoriales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True, null=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Tutoriales',
            },
        ),
        migrations.CreateModel(
            name='Tutoriales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True, null=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('titulo', models.CharField(max_length=200)),
                ('subtitulo', models.CharField(max_length=500)),
                ('urlvideo', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='URL Youtube')),
                ('archivo_video', models.FileField(blank=True, default='', null=True, upload_to='tutoriales/', verbose_name='Archivo de Video')),
                ('tipo', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='generales.Tipos_tutoriales')),
            ],
            options={
                'verbose_name_plural': 'Tutoriales',
            },
        ),
    ]
