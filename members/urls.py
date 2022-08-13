from django.urls import path
from .views import *

urlpatterns = [
    # User things view ----------------------------------------------------------------------
    path('login_user/', login_user, name='login'),  # Login user path
    path('logout_user/', logout_user, name='logout'),  # Logout user path
    path('register_user/', register_user, name='register'),  # Register user path
    path('search_users/', search_users, name='search_users'),  # Search users path
    # Change password view ------------------------------------------------------------------
    path('change_password/', PasswordsChangeView.as_view(), name='change_password'),  # Change users password path
    # (Not reset password)
    # Profile view --------------------------------------------------------------------------
    path('profile/', ProfileView.as_view(), name='profile'),  # Users profile path
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),  # Edit users profile path
    path('personal_page/<str:username>/', PersonalPageListView.as_view(), name='personal_page'),  # Users personal page
    # Post views ----------------------------------------------------------------------------
    path('social/', PostListView.as_view(), name='social'),  # Social path
    path('social/post/new/', PostCreateView.as_view(), name='create_post'),  # Create post path
    path('social/post/<int:pk>/', PostDetailView.as_view(), name='post_detail_view'),  # Detail post path
    path('social/post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit_view'),  # Edit post path
    path('social/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_view'),  # Delete post path
    # ---------------------------------------------------------------------------------------
]
