# Generated by Django 3.1.1 on 2020-10-19 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20201019_1133'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alternative',
            unique_together={('qid', 'text')},
        ),
    ]
