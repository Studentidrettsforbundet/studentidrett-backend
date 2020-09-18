# Generated by Django 3.1.1 on 2020-09-18 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20200918_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='team',
            field=models.ManyToManyField(blank=True, to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='tryoutdates',
            name='team',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team'),
        ),
    ]
