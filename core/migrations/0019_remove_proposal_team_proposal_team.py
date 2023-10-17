# Generated by Django 4.2.4 on 2023-10-13 05:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_section_word_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='team',
        ),
        migrations.AddField(
            model_name='proposal',
            name='team',
            field=models.ManyToManyField(related_name='proposals', to=settings.AUTH_USER_MODEL),
        ),
    ]