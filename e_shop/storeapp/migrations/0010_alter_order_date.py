# Generated by Django 5.1.2 on 2024-11-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0009_alter_product_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
