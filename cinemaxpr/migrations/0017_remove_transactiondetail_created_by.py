# Generated by Django 2.2.7 on 2019-11-12 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0016_auto_20191113_0448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiondetail',
            name='created_by',
        ),
    ]
