from django.shortcuts import render,redirect
from .models import Cart
from products.models import Products
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def shopping_cart(request):
    carts = Cart.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"orders/cart.html",{"carts":carts})

@login_required
def add_to_cart(request,product_id):
    product = Products.objects.get(id=product_id)
    cart_data ={
        "user":request.user,
        "product":product,
        "cart_qty":1,
        "cart_total":product.price,
    }
    Cart.objects.create(**cart_data)
    return redirect("/cart")

def checkout(request):
    return render(request,"orders/checkout.html")

def order_summary(request):
    return render(request,"orders/orders.html")


