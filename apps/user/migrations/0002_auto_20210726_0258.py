# Generated by Django 3.2.5 on 2021-07-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='occupation',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Administrador'), (1, 'Especialista'), (2, 'Estudiante')], default=2, verbose_name='role'),
        ),
    ]
