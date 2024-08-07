# Generated by Django 4.2.4 on 2024-07-11 05:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_proposal_submission_date_alter_profiletheme_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 18, 5, 48, 52, 205341, tzinfo=datetime.timezone.utc)),
        ),
    ]
