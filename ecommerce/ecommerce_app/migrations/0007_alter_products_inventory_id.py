# Generated by Django 4.2.3 on 2023-09-26 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0006_products_inventory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='inventory_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce_app.inventory'),
        ),
    ]
