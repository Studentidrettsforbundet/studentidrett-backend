# Generated by Django 3.1.1 on 2020-09-10 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubSports', '0004_auto_20200910_1723'),
        ('interest', '0004_auto_20200909_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interest',
            options={'ordering': ['club_sport']},
        ),
        migrations.RemoveField(
            model_name='interest',
            name='club',
        ),
        migrations.RemoveField(
            model_name='interest',
            name='sport',
        ),
        migrations.AddField(
            model_name='interest',
            name='club_sport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clubSports.clubsport'),
            preserve_default=False,
        ),
    ]
