# Generated by Django 5.1.3 on 2024-11-19 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Characters', '0015_remove_inventarioalimento_objeto_inventario_objeto'),
    ]

    operations = [
        migrations.AddField(
            model_name='objeto',
            name='cantidad_disponible',
            field=models.IntegerField(default=10),
        ),
    ]
