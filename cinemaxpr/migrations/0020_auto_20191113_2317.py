# Generated by Django 2.2.7 on 2019-11-13 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0019_auto_20191113_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiondetail',
            name='memo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.MemoDetail'),
        ),
    ]
