# urls.py
from django.urls import path
from .views import CompleteSignupView, SignupView, LoginView, LogoutView, change_password, reset_password, set_password, complete_signup

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('complete-signup/', CompleteSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('set-password/', set_password, name='set-password'),
    path('complete-signup/', complete_signup, name='complete_signup'),
]
