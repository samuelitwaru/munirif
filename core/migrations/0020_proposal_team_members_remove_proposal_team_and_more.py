# Generated by Django 4.2.4 on 2023-10-17 05:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0019_remove_proposal_team_proposal_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='team_members',
            field=models.ManyToManyField(related_name='team_proposals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='team',
        ),
        migrations.AddField(
            model_name='proposal',
            name='team',
            field=models.TextField(blank=True, null=True),
        ),
    ]
