# Generated by Django 2.2.7 on 2019-11-18 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0034_auto_20191119_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessunit',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
