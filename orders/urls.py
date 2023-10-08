from django.urls import path
from users.views import home,user_login,user_register

urlpatterns = [
    path('',home,name = "home_page"),
    path('login/',user_login,name = "login_page"),
    path('register/',user_register,name = "register_page"),
    
]
