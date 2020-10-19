# Generated by Django 3.1.1 on 2020-10-19 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='left',
        ),
        migrations.RemoveField(
            model_name='question',
            name='right',
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='answer',
            name='qid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='questionnaire.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=100),
        ),
    ]
