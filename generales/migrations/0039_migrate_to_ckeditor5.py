# Migración manual: cambia los campos RichTextField (CKEditor 4) por CKEditor5Field
# en todos los modelos. Sin cambio de tipo en PostgreSQL (ambos son TEXT).

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0038_io_funcionarios_eventos_almuerzo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sedes',
            name='descripcion',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True),
        ),
        migrations.AlterField(
            model_name='noticias',
            name='descripcion',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='nuestra_empresa',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Nuestra Empresa'),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='mision',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Mision'),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='vision',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Vision'),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='objetivo',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Objetivo General'),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='principios',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Principios y Fundamentos'),
        ),
        migrations.AlterField(
            model_name='miempresa',
            name='himno_letra',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Letra Himno Sistema INRAI'),
        ),
        migrations.AlterField(
            model_name='home1',
            name='nuestra_empresa',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=3000, null=True, verbose_name='Nuestra Empresa'),
        ),
        migrations.AlterField(
            model_name='home1',
            name='comunicaciones',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=3000, null=True, verbose_name='Comunicaciones'),
        ),
        migrations.AlterField(
            model_name='home1',
            name='marketing',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=3000, null=True, verbose_name='Marketing'),
        ),
        migrations.AlterField(
            model_name='home1',
            name='entretenimiento',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=3000, null=True, verbose_name='Entretenimiento'),
        ),
        migrations.AlterField(
            model_name='bienestar',
            name='detalle',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Detalle'),
        ),
        migrations.AlterField(
            model_name='ocupacional',
            name='detalle',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=15000, null=True, verbose_name='Detalle'),
        ),
        migrations.AlterField(
            model_name='elmuro',
            name='detalle',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=5000, null=True, verbose_name='Detalle'),
        ),
        migrations.AlterField(
            model_name='reglamento',
            name='reglamento',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=200000, null=True, verbose_name='Reglamento Interno de Trabajo'),
        ),
    ]
