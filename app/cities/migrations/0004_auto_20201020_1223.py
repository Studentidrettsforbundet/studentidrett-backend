# Generated by Django 3.1.2 on 2020-10-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0003_auto_20201007_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
