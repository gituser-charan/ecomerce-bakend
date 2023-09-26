# Generated by Django 4.2.3 on 2023-09-26 05:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_rename_variant_cartitem_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('profile', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='productdetails',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='productdetails',
            old_name='title_details',
            new_name='name_details',
        ),
        migrations.RenameField(
            model_name='subcategories',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='subcategories',
            name='is_active',
        ),
        migrations.AddField(
            model_name='subcategories',
            name='modified_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]