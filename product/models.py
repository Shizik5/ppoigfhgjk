from registration.models import CustomUser
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Катерогии'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return f' ваш товар {self.category} - {self.title}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.user} - {self.product.category} { self.product.title} " \
               f"- количество-{self.quantity} - цена :{self.quantity * self.product.price}"

    class Meta:
        verbose_name = ('Корзина')
        verbose_name_plural = ('Корзины')
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        existing_cart_item = CartItem.objects.filter(user=self.user, product=self.product).first()

        if existing_cart_item:
            existing_cart_item.quantity += self.quantity
            existing_cart_item.save()
        else:
            super().save(*args, **kwargs)

