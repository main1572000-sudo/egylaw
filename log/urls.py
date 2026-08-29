from django.urls import path
from . import views
from django.contrib.auth.views import LoginView ,LogoutView ,PasswordChangeView,PasswordChangeDoneView
# from .views import CustomLogoutView
urlpatterns = [
    path('register/',views.registration,name='register'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('changepw/', PasswordChangeView.as_view(template_name='change_password.html'), name='changepw'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]