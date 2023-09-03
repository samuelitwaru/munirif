# urls.py
from django.urls import path
from .views import SignupView, LoginView, LogoutView, change_password, reset_password, set_password

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('set-password/', set_password, name='set-password'),
]
