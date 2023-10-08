from django.urls import path
from users.views import new_arrival_product,product_detail

urlpatterns = [
   
    path('new-arrival/',new_arrival_product,name = "new-arrival_page"),
    path('product-detail/',product_detail,name = "product-detail_page"),
    
]
