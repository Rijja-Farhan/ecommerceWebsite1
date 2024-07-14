from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('W', 'Women'),
    ('M', 'Men'),
    ('K', 'Kids'),
]

class Item(models.Model):
    name = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='W')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(default='')
    slug = models.SlugField() 

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):  
        return f"{self.quantity} of {self.item.name}" 

    def get_total_item_price(self):
        return self.quantity * self.item.price
    

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    orderNumber = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
  

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username