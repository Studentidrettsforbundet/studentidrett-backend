# Generated by Django 3.1.1 on 2020-09-09 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_auto_20200909_1509'),
        ('interest', '0003_auto_20200909_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club'),
        ),
    ]
