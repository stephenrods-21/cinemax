# Generated by Django 2.2.7 on 2019-11-10 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0005_auto_20191110_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.Role'),
        ),
    ]
