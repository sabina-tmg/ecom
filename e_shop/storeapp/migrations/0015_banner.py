# Generated by Django 5.1.2 on 2024-11-08 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0014_alter_orderitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='banners/banner')),
            ],
        ),
    ]
