# Generated by Django 3.1.1 on 2020-09-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubSports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('club_sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubSports.clubsport')),
            ],
            options={
                'ordering': ['club_sport'],
            },
        ),
    ]
