from django.db import models
from products.models import Products
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart_qty = models.IntegerField(default=0)
    cart_total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.Products.title
    
class Orders(models.Model):
    ORDER_STATUS =[("PENDING","PENDING"),("DELIVERED","DELIVERED"),("ON_THE_WAY","ON THE WAY"),("CANCELLED","CANCELLED")]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.JSONField()
    total_amount = models.FloatField(default=0)
    shipping_address=models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    additional_info= models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20,default="COD")
    status=models.CharField(max_length=20,choices=ORDER_STATUS,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk
