# Generated by Django 4.2.4 on 2023-10-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_proposal_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('EDITING', 'EDITING'), ('SUBMITTED', 'SUBMITTED'), ('SCORING', 'SCORING'), ('REVIEWED', 'REVIEWED')], default='EDITING', max_length=64),
        ),
    ]