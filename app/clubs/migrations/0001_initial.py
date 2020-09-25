# Generated by Django 3.1.1 on 2020-09-23 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1023, null=True)),
                ('contact_email', models.EmailField(max_length=127, null=True)),
                ('pricing', models.CharField(max_length=255, null=True)),
                ('register_info', models.CharField(max_length=255, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubs', to='cities.city')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
