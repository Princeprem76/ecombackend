from django.db import models

# Create your models here.
from user.models import UserEmail


class subcategory(models.Model):
    sub_category_name = models.CharField(max_length=120)

    def __str__(self):
        return self.sub_category_name


class category(models.Model):
    category_name = models.CharField(max_length=150)
    sub_category = models.ManyToManyField(subcategory)

    def __str__(self):
        return self.category_name


class productImage(models.Model):
    product_image = models.ImageField(upload_to='product/')




class products(models.Model):
    product_name = models.CharField(max_length=150)
    product_image = models.ManyToManyField(productImage)
    product_quantity = models.PositiveIntegerField()
    product_price = models.PositiveIntegerField()
    product_discount = models.PositiveIntegerField(default=0)
    product_category = models.ForeignKey(category, on_delete=models.CASCADE)
    is_top_selling = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    def get_discounted_price(self):
        price = self.product_price - (self.product_discount * 0.01 * self.product_price)
        return price

    def get_image_count(self):
        cou = self.product_image.all().count()
        return cou


class wishlist(models.Model):
    user = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    product = models.ManyToManyField(products)

    def __str__(self):
        return self.user.email
