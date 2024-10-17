from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'), # /store/
    
    path('signup/', views.signup, name='signup'), # /store/signup/
    
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'), # /store/product/1/product-name/
    path('accounts/logout/', views.logout_view, name='logout'),
]
