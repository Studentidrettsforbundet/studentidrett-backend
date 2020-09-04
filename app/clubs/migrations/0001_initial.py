# Generated by Django 3.1.1 on 2020-09-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=11)),
                ('pricing', models.FloatField(null=True)),
                ('register_info', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]