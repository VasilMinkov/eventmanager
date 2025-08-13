from django.contrib.auth.views import LogoutView
from django.urls import path
from eventmanager.accounts import views
from eventmanager.accounts.views import UserProfileView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
