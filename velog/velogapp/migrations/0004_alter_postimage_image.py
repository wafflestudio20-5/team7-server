# Generated by Django 4.1 on 2023-02-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velogapp', '0003_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]