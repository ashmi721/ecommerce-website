from django.shortcuts import render

# Create your views here.
def shopping_cart(request):
    return render(request,"orders/cart.html")

def checkout(request):
    return render(request,"orders/checkout.html")

def order_summary(request):
    return render(request,"orders/orders.html")


