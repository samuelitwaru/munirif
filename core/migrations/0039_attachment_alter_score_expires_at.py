# Generated by Django 4.2.4 on 2024-07-05 04:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_score_expires_at_alter_section_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('max_size', models.IntegerField(default=5000)),
            ],
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 12, 4, 0, 48, 301249, tzinfo=datetime.timezone.utc)),
        ),
    ]
