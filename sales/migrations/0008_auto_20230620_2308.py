# Generated by Django 3.2 on 2023-06-20 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_order_delivery_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='with_size',
            field=models.BooleanField(default=False),
        ),
    ]
