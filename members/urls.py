from django.urls import path
from .views import *

urlpatterns = [
    # User auth view ------------------------------------------------------------------------
    path('login_user/', login_user, name='login'),  # Login user path
    path('logout_user/', logout_user, name='logout'),  # Logout user path
    path('register_user/', register_user, name='register'),  # Register user path
    path('search_users/', search_users, name='search_users'),  # Search users path
    # Change password view  (Not reset password) --------------------------------------------
    path('change_password/', PasswordsChangeView.as_view(), name='change_password'),
    # Profile view --------------------------------------------------------------------------
    path('profile/', ProfileView.as_view(), name='profile'),  # Users profile
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),  # Edit users profile
]
