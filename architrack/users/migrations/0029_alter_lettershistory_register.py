# Generated by Django 4.0.3 on 2022-03-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_modality_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettershistory',
            name='register',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]