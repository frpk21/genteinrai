# Generated by Django 2.2.1 on 2022-08-15 03:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0004_auto_20220814_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='sedes',
            name='descripcion',
            field=ckeditor.fields.RichTextField(blank=True, max_length=15000, null=True),
        ),
    ]
