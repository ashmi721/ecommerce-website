from django.urls import path
from .views import shopping_cart,checkout,order_summary

urlpatterns = [
    path('cart/',shopping_cart,name = "cart_page"),
    path('checkout/',checkout,name = "checkout_page"),
    path('order-summary/',order_summary,name = "order_summary_page"),
    
]
