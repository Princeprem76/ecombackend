# Generated by Django 4.0.5 on 2022-06-24 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_payment_payment_method_order_payment_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='current_order',
        ),
    ]