from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'), # /cart/
    path('add/<int:product_id>/', views.cart_add, name='cart_add'), # /cart/add/1/
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'), # /cart/remove/1/
]