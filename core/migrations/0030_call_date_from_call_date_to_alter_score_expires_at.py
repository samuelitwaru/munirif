# Generated by Django 4.2.4 on 2024-06-24 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_proposal_call_alter_score_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='date_from',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='call',
            name='date_to',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 13, 43, 18, 57768, tzinfo=datetime.timezone.utc)),
        ),
    ]
