from django.urls import path
from . import views
from django.contrib.auth.views import LoginView ,LogoutView
# from .views import CustomLogoutView
urlpatterns = [
    path('register/',views.registration,name='register'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]