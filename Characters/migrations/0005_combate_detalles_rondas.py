# Generated by Django 5.1.3 on 2024-11-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Characters', '0004_rename_puntos_vida_enemigo_puntos_de_vida'),
    ]

    operations = [
        migrations.AddField(
            model_name='combate',
            name='detalles_rondas',
            field=models.JSONField(default=list),
        ),
    ]
