# Generated by Django 4.2.4 on 2023-09-01 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce_app', '0005_alter_customuser_address_alter_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
