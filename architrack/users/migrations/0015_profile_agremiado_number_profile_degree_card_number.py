# Generated by Django 4.0.1 on 2022-01-18 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_course_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='agremiado_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='degree_card_number',
            field=models.CharField(blank=True, default='0000000', max_length=50, null=True),
        ),
    ]
