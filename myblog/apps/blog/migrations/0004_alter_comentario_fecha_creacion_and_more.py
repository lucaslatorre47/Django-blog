# Generated by Django 5.1.1 on 2024-10-23 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comentario_fecha_creacion_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 23, 19, 34, 22, 109800, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 23, 19, 34, 22, 108801, tzinfo=datetime.timezone.utc)),
        ),
    ]
