# Generated by Django 2.2.1 on 2022-08-18 16:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0011_auto_20220817_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bienestar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True, null=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('titulo', models.CharField(max_length=200)),
                ('detalle', ckeditor.fields.RichTextField(blank=True, max_length=15000, null=True, verbose_name='Detalle')),
                ('foto', models.FileField(blank=True, default='', null=True, upload_to='fotos/', verbose_name='Foto')),
            ],
            options={
                'verbose_name_plural': 'Bienestar Social',
            },
        ),
        migrations.CreateModel(
            name='Ocupacional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reglamento', ckeditor.fields.RichTextField(blank=True, max_length=15000, null=True, verbose_name='Reglamento Interno de Trabajo')),
            ],
            options={
                'verbose_name_plural': 'Reglamento',
            },
        ),
    ]
