# Generated by Django 3.2.9 on 2021-12-14 05:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_year_profile_years'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('institution', models.CharField(max_length=200, null=True)),
                ('hours', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('A', 'Active'), ('I', 'Inactive')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='training_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='courses',
            field=models.ManyToManyField(blank=True, to='users.Course'),
        ),
    ]
