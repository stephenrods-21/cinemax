# Generated by Django 2.2.7 on 2019-11-13 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0020_auto_20191113_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='email',
            field=models.CharField(default='test@test.com', max_length=75),
            preserve_default=False,
        ),
    ]
