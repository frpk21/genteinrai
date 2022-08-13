# Generated by Django 2.2.1 on 2022-08-12 14:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0004_auto_20220812_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionarios',
            name='fecha_nacimiento',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de nacimiento'),
            preserve_default=False,
        ),
    ]
