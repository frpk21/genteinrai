# Generated by Django 2.2.1 on 2022-08-15 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0005_sedes_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='sedes',
            name='foto1',
            field=models.FileField(default='', upload_to='fotos/', verbose_name='Foto Sede (476x570)'),
        ),
        migrations.AddField(
            model_name='sedes',
            name='foto2',
            field=models.FileField(default='', upload_to='fotos/', verbose_name='Foto Sede (476x570)'),
        ),
        migrations.AddField(
            model_name='sedes',
            name='foto3',
            field=models.FileField(default='', upload_to='fotos/', verbose_name='Foto Sede (476x570)'),
        ),
    ]