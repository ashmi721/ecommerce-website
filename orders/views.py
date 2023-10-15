from django.shortcuts import render,redirect
from .models import Cart
from products.models import Products
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def shopping_cart(request):
    carts = Cart.objects.filter(user=request.user).order_by("created_at")
    has_items = len(carts) >0
    total_cart_amount =0
    grand_total= 0
    vat_amount = 0
    if has_items:
        # total_cart_amount = sum([Cart.cart_total for cart in carts])
        for item in carts:
            total_cart_amount += item.cart_total
        vat_amount = total_cart_amount * 0.13
        grand_total = total_cart_amount + vat_amount
    return render(request,"orders/cart.html",{"carts":carts,"has_items":has_items,"total_cart_amount":total_cart_amount,"vat_amount":vat_amount,"grand_total":grand_total})

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

def remove_cart(request,cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    return redirect("/cart")

def checkout(request):
    return render(request,"orders/checkout.html")

def order_summary(request):
    return render(request,"orders/orders.html")


