# Generated by Django 2.2.1 on 2022-08-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0013_auto_20220818_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='bienestar',
            name='tipo',
            field=models.CharField(choices=[('news', 'Noticias'), ('event', 'Eventos'), ('insp', 'Medio Ambiente')], default='news', max_length=5),
        ),
    ]