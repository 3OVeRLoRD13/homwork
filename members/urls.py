from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name='login'),
    path('logout_user/', logout_user, name='logout'),
    path('register_user/', register_user, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('search_users/', search_users, name='search_users'),
    path('personal_page/', PersonalPageListView.as_view(), name='personal_page'),
    path('social/', PostListView.as_view(), name='social'),
    path('social/post/new/', PostCreateView.as_view(), name='create_post'),
    path('social/post/<int:pk>/', PostDetailView.as_view(), name='post_detail_view'),
    path('social/post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit_view'),
    path('social/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_view'),
]
