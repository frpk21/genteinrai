# Generated by Django 2.2.1 on 2022-08-25 15:06

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0018_auto_20220825_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elmuro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True, null=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('titulo', models.CharField(max_length=200)),
                ('detalle', ckeditor.fields.RichTextField(blank=True, max_length=15000, null=True, verbose_name='Detalle')),
                ('foto', models.FileField(blank=True, default='', null=True, upload_to='fotos/', verbose_name='Foto (417 x 269px)')),
            ],
            options={
                'verbose_name_plural': 'El Muro',
            },
        ),
    ]