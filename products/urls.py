from django.urls import path
from .views import new_arrival_product,product_detail

urlpatterns = [
   
    path('new-arrival/',new_arrival_product,name = "new_arrival_page"),
    path('product-detail/',product_detail,name = "product_detail_page"),
    
]
