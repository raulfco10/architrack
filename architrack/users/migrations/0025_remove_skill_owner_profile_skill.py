# Generated by Django 4.0.2 on 2022-02-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_profile_agremiado_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='owner',
        ),
        migrations.AddField(
            model_name='profile',
            name='skill',
            field=models.ManyToManyField(blank=True, to='users.Skill'),
        ),
    ]
