from django.shortcuts import render

# Create your views here.
def new_arrival_product(request):
    return render(request,"new-arrival.html")

def product_detail(request):
    return render(request,"product-detail.html")