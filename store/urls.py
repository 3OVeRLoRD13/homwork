from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.show_products, name='ShowProducts'),
    path('product/<int:pk>/<int:pg>/', views.show_detail_of_product, name='show_detail_of_product'),
    path('like_product/<int:pk>/<int:pg>/', views.like_product, name='like_product')
]
