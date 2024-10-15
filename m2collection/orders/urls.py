from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'), # /orders/create/
    path('<int:order_id>/', views.order_detail, name='order_detail'), # /orders/1/
]