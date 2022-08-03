from django.urls import path
from members.views import *

urlpatterns = [
    path('login_user/', login_user, name='login'),
    path('logout_user/', logout_user, name='logout'),
    path('register_user/', register_user, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
]
