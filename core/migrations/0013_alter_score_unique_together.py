# Generated by Django 4.2.4 on 2023-09-03 03:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_score_capacity_development_comment_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('user', 'proposal')},
        ),
    ]
