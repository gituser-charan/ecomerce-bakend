# Generated by Django 4.2.3 on 2023-09-26 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0007_remove_orderitem_line_total_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='variant',
            new_name='products',
        ),
    ]
