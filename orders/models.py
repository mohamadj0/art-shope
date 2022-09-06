from django.db import models
from accounts.models import User
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'
    
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return (total - discount_price)
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.price}'
    
    def get_cost(self):
        return self.price * self.quantity

class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])

    def __str__(self):
        return self.code












