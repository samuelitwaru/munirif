# Generated by Django 4.2.4 on 2024-07-07 08:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_call_review_date_call_selection_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='lower_limit',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='score',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 14, 8, 20, 14, 805823, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='section',
            name='word_limit',
            field=models.IntegerField(default=250),
        ),
        migrations.AlterField(
            model_name='team',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_set', to='core.proposal'),
        ),
    ]
