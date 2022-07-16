from django.db import models

# Create your models here.
from product.models import products
from user.models import UserEmail


class location(models.Model):
    user = models.ForeignKey(UserEmail, on_delete=models.CASCADE,
                             null=True, )
    email = models.EmailField(null=True)
    name = models.CharField(max_length=150)
    phone = models.PositiveBigIntegerField()
    drop_location = models.CharField(max_length=250)

    def __str__(self):
        return str(self.drop_location)


class items(models.Model):
    user = models.ForeignKey(UserEmail, on_delete=models.SET_NULL,
                             null=True, )
    item = models.ForeignKey(products, on_delete=models.SET_NULL,
                             null=True, )
    quantity = models.PositiveIntegerField(default=0)
    item_size = models.CharField(max_length=150, null=True)
    item_color = models.CharField(max_length=150, null=True)
    current_order = models.BooleanField(default=False)

    def __str__(self):
        return self.item.product_name

    def get_total(self):
        return self.quantity * self.item.get_discounted_price()


class orders(models.Model):
    order_code = models.CharField(max_length=10, null=True)
    order_by = models.ForeignKey(UserEmail, on_delete=models.SET_NULL,
                                 null=True)
    item = models.ManyToManyField(items)
    order_date = models.DateField(null=True)
    order_end = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    drop_location = models.ForeignKey(location, on_delete=models.SET_NULL,
                                      null=True)

    # def __str__(self):
    #     return self.order_by.email

    def get_total(self):
        totals = 0
        for it in self.item.all():
            totals += it.get_total()
        return totals


class coupon(models.Model):
    coupon_number = models.CharField(max_length=8)
    discount = models.PositiveSmallIntegerField()
    generated_date = models.DateTimeField(auto_now=True)
    is_Expired = models.BooleanField(default=False)

    def __str__(self):
        return str(self.coupon_number)


class order_payment(models.Model):
    user = models.ForeignKey(UserEmail, on_delete=models.SET_NULL,
                             null=True, )
    payment_id = models.CharField(max_length=150)
    payment_by = models.CharField(max_length=150)
    amount = models.PositiveIntegerField()
    order_code = models.CharField(max_length=10)
    payment_token = models.CharField(max_length=20, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=120, null=True)

    def __str__(self):
        return 'Amount {} Paid for Order ID {} on {}'.format(self.amount, self.order_code, self.payment_date)
