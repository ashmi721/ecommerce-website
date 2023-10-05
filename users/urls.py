from django.urls import path
from users.views import home

urlpatterns = [
    path('',home,name = "home_page"),
]
