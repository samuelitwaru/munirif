# Generated by Django 4.2.4 on 2023-09-02 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_sections_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='capacity_development_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='conflict_of_interest_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='detailed_budget_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='ethical_implications_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='outputs_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='problem_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='scalability_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='solution_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='summary_budget_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='team_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='workplan_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
