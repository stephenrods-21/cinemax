# Generated by Django 2.2.7 on 2019-11-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0010_businessunit_documentno'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineofapprovaldetail',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
