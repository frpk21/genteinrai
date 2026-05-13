# Migración manual: amplía choices de io_funcionarios.tipo_evento
# para incluir inicio/fin de almuerzo y "otro". Sin pérdida de datos.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0037_rename_tio_evento_io_funcionarios_tipo_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='io_funcionarios',
            name='tipo_evento',
            field=models.IntegerField(
                choices=[
                    (0, 'Entrada'),
                    (1, 'Salida'),
                    (2, 'Inicio Almuerzo'),
                    (3, 'Fin Almuerzo'),
                    (4, 'Otro'),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name='io_funcionarios',
            name='fecha',
            field=models.DateField(verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='io_funcionarios',
            name='hora',
            field=models.TimeField(verbose_name='Hora'),
        ),
        migrations.AlterModelOptions(
            name='io_funcionarios',
            options={
                'ordering': ['fecha', 'hora'],
                'verbose_name_plural': 'Eventos de Asistencia',
            },
        ),
    ]
