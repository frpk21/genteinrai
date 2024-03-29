# Generated by Django 3.2.19 on 2024-02-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0032_funcionarios_cedula'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funcionarios',
            options={'verbose_name_plural': 'Funcionarios'},
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='hora_entrada',
            field=models.TimeField(default='07:00', verbose_name='Hora de entrada (inicio jornada)'),
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='hora_entrada_de_almuerzo',
            field=models.TimeField(blank=True, default='14:00', verbose_name='Hora entreda de almuerzo'),
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='hora_salida',
            field=models.TimeField(default='18:00', verbose_name='Hora salida (terminación jornada)'),
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='hora_salida_almuerzo',
            field=models.TimeField(blank=True, default='12:00', verbose_name='Hora de salida almuerzo'),
        ),
        migrations.AlterField(
            model_name='funcionarios',
            name='cedula',
            field=models.CharField(default='', max_length=50, verbose_name='Cédula No. (ID) '),
        ),
        migrations.AlterField(
            model_name='funcionarios',
            name='fecha_ultimo_carnet',
            field=models.DateField(blank=True, verbose_name='Fecha de emisión del último carnet'),
        ),
        migrations.AlterField(
            model_name='funcionarios',
            name='foto',
            field=models.FileField(default='', upload_to='fotos/', verbose_name='Archivo con Foto del Funcionario (250 x 250px  FONDO BLANCO)'),
        ),
        migrations.AlterField(
            model_name='funcionarios',
            name='tipo_contrato',
            field=models.IntegerField(choices=[(0, 'Indefinido'), (1, 'Fijo'), (2, 'Aprendiz SENA')], default=0),
        ),
    ]
