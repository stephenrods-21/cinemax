# Generated by Django 2.2.7 on 2019-11-17 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaxpr', '0032_auto_20191117_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondetail',
            name='purchaseRequisitionDetail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.PurchaseRequisitionDetail'),
        ),
        migrations.AlterField(
            model_name='transactiondetail',
            name='memoObj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cinemaxpr.MemoDetail'),
        ),
    ]
