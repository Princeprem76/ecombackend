# Generated by Django 4.0.5 on 2022-06-16 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_wishlist_product_wishlist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_top_selling',
            field=models.BooleanField(default=False),
        ),
    ]
