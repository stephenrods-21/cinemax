# Generated by Django 2.2.7 on 2019-11-12 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0013_budgetdetail_memodetail_transactiondetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondetail',
            name='lineOfApproval',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.LineOfApproval'),
            preserve_default=False,
        ),
    ]
