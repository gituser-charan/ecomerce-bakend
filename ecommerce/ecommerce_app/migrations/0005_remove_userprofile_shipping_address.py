# Generated by Django 4.2.3 on 2023-09-21 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_remove_customuser_address_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='shipping_address',
        ),
    ]