# Generated by Django 3.1.1 on 2020-09-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20200918_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='tryout_dates',
            field=models.ManyToManyField(to='teams.TryoutDates'),
        ),
    ]