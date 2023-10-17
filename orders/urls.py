from django.urls import path
from .views import shopping_cart,checkout,order_summary,add_to_cart,update_cart,remove_cart,purchase_now,thankyou

urlpatterns = [
    path('cart/',shopping_cart,name = "cart_page"),
    path('checkout/',checkout,name = "checkout_page"),
    path('order-summary/',order_summary,name = "order_summary_page"),
    path("add-to-cart/<int:product_id>",add_to_cart,name="add_to_cart_page"),
    path("update-cart/<int:cart_id>",update_cart,name="update_cart_page"),
    path("remove-cart/<int:cart_id>",remove_cart,name="remove_cart_page"),
    path("purchase/",purchase_now,name = "purchase_page"),
    path("thank-you/",thankyou, name="thank_you_page"),

]
