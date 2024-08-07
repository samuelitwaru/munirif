# Generated by Django 4.2.4 on 2024-07-06 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_score_expires_at_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='review_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='call',
            name='selection_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='call',
            name='submission_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 13, 8, 48, 35, 996847, tzinfo=datetime.timezone.utc)),
        ),
    ]
