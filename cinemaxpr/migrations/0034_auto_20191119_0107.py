# Generated by Django 2.2.7 on 2019-11-18 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0033_auto_20191117_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='businessunit',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.businessunit'),
        ),
        migrations.AlterField(
            model_name='lineofapproval',
            name='businessunit',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.businessunit'),
        ),
        migrations.AlterField(
            model_name='memodetail',
            name='businessunit',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.businessunit'),
        ),
        migrations.AlterField(
            model_name='transactiondetail',
            name='businessunitObj',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
