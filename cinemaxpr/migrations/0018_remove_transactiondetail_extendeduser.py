# Generated by Django 2.2.7 on 2019-11-12 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0017_remove_transactiondetail_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiondetail',
            name='extendeduser',
        ),
    ]
