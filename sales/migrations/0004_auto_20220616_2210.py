# Generated by Django 3.2 on 2022-06-16 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_product_mode_paiement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='mode_paiement',
        ),
        migrations.AddField(
            model_name='order',
            name='mode_paiement',
            field=models.CharField(default='', max_length=200),
        ),
    ]