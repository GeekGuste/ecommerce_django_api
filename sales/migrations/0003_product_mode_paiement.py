# Generated by Django 3.2 on 2022-06-15 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='mode_paiement',
            field=models.CharField(default='', max_length=200),
        ),
    ]
