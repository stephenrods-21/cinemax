# Generated by Django 2.2.7 on 2019-11-13 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0021_extendeduser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactiondetail',
            old_name='businessunit',
            new_name='businessunitObj',
        ),
        migrations.RenameField(
            model_name='transactiondetail',
            old_name='extendeduser',
            new_name='extendeduserObj',
        ),
        migrations.RenameField(
            model_name='transactiondetail',
            old_name='memo',
            new_name='memoObj',
        ),
    ]
