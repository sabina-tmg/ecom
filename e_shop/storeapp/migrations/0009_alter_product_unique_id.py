# Generated by Django 5.1.2 on 2024-11-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0008_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unique_id',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]