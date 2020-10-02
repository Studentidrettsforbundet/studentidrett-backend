# Generated by Django 3.1.1 on 2020-10-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('region', models.CharField(choices=[('nord', 'Nord-Norge'), ('midt', 'Midt-Norge'), ('vest', 'Vestlandet'), ('sør', 'Sørlandet'), ('øst', 'Østlandet')], max_length=4)),
            ],
            options={
                'ordering': ['region'],
            },
        ),
    ]
