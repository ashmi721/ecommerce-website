from django.shortcuts import render
from .models import Products
# Create your views here.
def new_arrival_product(request):
    return render(request,"products/new-arrival.html")

def product_detail(request,product_id):
    products = Products.objects.get(id = product_id)
    return render(request,"products/product-detail.html",{"products":products})
