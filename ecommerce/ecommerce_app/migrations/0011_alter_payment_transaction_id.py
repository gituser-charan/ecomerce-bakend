# Generated by Django 4.2.3 on 2023-09-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0010_remove_orderitem_order_order_order_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Transaction_id',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]