# Generated by Django 3.1.1 on 2020-10-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_auto_20201005_2318'),
        ('questionnaire', '0007_auto_20201019_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='sports',
            field=models.ManyToManyField(related_name='labels', to='sports.Sport'),
        ),
    ]