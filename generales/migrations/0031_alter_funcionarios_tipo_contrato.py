# Generated by Django 3.2.19 on 2024-02-04 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0030_funcionarios_fecha_ultimo_carnet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionarios',
            name='tipo_contrato',
            field=models.IntegerField(choices=[(0, 'Indefinido'), (1, 'Fijo')], default=0),
        ),
    ]
