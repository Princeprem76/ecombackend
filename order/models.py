from django.db import models

# Create your models here.
from product.models import products
from user.models import UserEmail


class items(models.Model):
    user = models.ForeignKey(UserEmail, on_delete=models.SET_NULL,
                             null=True, )
    item = models.ForeignKey(products, on_delete=models.SET_NULL,
                             null=True, )
    quantity = models.PositiveIntegerField()
    current_order = models.BooleanField(default=False)

    def __str__(self):
        return self.item.product_name

    def get_total(self):
        return self.quantity * self.item.product_price


class orders(models.Model):
    order_code = models.CharField(max_length=10)
    order_by = models.ForeignKey(UserEmail, on_delete=models.SET_NULL,
                                 null=True)
    item = models.ManyToManyField(items)
    order_date = models.DateField()
    order_end = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.order_by.email

    def get_total(self):
        totals = 0
        for it in self.item.all():
            totals += it.get_total()
        return totals


class location(models.Model):
    order = models.ForeignKey(orders, on_delete=models.SET_NULL,
                              null=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=150)
    phone = models.PositiveBigIntegerField()
    drop_location = models.CharField(max_length=250)

    def __str__(self):
        return str(self.drop_location)


class coupon(models.Model):
    coupon_number = models.CharField(max_length=8)
    discount = models.PositiveSmallIntegerField()
    generated_date = models.DateTimeField(auto_now=True)
    is_Expired = models.BooleanField(default=False)

    def __str__(self):
        return str(self.coupon_number)


class order_payment(models.Model):
    payment_id = models.CharField(max_length=150)
    payment_by = models.PositiveBigIntegerField()
    amount = models.PositiveIntegerField()
    order_code = models.CharField(max_length=10)
    payment_token = models.CharField(max_length=20, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Amount {} Paid for Order ID {} on {}'.format(self.amount, self.order_code, self.payment_date)
