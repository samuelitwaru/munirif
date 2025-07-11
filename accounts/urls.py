# urls.py
from django.urls import path
from .views import CompleteSignupView, SignupView, LoginView, LogoutView, change_password, reset_password, set_password, complete_signup, update_user, send_email_notifications

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('complete-signup/', CompleteSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change-password'),
    path('update-user/', update_user, name='update-user'),
    path('reset-password/', reset_password, name='reset-password'),
    path('set-password/', set_password, name='set-password'),
    path('complete-signup/', complete_signup, name='complete_signup'),
    path('send-email-notifications/', send_email_notifications, name='send_email_notifications'),

]
