# Generated by Django 4.0.5 on 2022-06-20 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0011_order_payment_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_payment',
            name='payment_method',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='order_payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order_payment',
            name='payment_by',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
