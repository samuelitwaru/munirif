# Generated by Django 4.2.4 on 2024-06-26 04:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_section_description_alter_profile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 3, 4, 48, 14, 241749, tzinfo=datetime.timezone.utc)),
        ),
    ]