# Generated by Django 4.2.4 on 2024-07-17 02:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_score_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 24, 2, 20, 40, 559368, tzinfo=datetime.timezone.utc)),
        ),
    ]
