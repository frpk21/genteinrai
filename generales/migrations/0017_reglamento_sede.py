# Generated by Django 2.2.1 on 2022-08-25 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0016_auto_20220825_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='reglamento',
            name='sede',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='generales.Sedes'),
        ),
    ]
