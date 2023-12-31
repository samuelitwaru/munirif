# Generated by Django 4.2.4 on 2023-08-12 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='subject',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='description',
        ),
        migrations.AddField(
            model_name='proposal',
            name='capacity_development',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='conflict_of_interest',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='detailed_budget',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='ethical_implications',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='outputs',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='scalability',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='summary_budget',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='team',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='workplan',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='problem',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='solution',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.IntegerField(null=True)),
                ('solution', models.IntegerField(null=True)),
                ('outputs', models.IntegerField(null=True)),
                ('team', models.IntegerField(null=True)),
                ('capacity_development', models.IntegerField(null=True)),
                ('scalability', models.IntegerField(null=True)),
                ('ethical_implications', models.IntegerField(null=True)),
                ('conflict_of_interest', models.IntegerField(null=True)),
                ('summary_budget', models.IntegerField(null=True)),
                ('detailed_budget', models.IntegerField(null=True)),
                ('workplan', models.IntegerField(null=True)),
                ('strengths', models.TextField(null=True)),
                ('weaknesses', models.TextField(null=True)),
                ('comment', models.TextField(null=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.proposal')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
