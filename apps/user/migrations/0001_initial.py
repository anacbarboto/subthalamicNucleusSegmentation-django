# Generated by Django 3.2.5 on 2021-07-26 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='auth.user')),
                ('phone', models.CharField(max_length=10, verbose_name='phone')),
                ('entity', models.CharField(max_length=50, verbose_name='entity')),
                ('occupation', models.PositiveSmallIntegerField(choices=[(0, 'Estudiante'), (1, 'Radiologo')], default=1, verbose_name='occupation')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
