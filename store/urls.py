from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.show_products, name='ShowProducts'),  # View products path
    path('product/<int:pk>/<int:pg>/', views.show_detail_of_product, name='show_detail_of_product'),  # View detail
    #  of products path
    path('like_product/<int:pk>/<int:pg>/', views.like_product, name='like_product')  # Like products
]
