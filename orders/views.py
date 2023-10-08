from django.shortcuts import render

# Create your views here.
def shopping_cart(request):
    return render(request,"cart.html")

def checkout(request):
    return render(request,"checkout.html")

def order_summary(request):
    return render(request,"orders.html")


