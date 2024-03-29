# Generated by Django 4.0.5 on 2022-07-16 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_wishlist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.subcategory'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category_name',
            field=models.CharField(max_length=150),
        ),
    ]
