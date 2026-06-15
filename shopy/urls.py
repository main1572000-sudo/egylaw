from django.urls import path
from . import views
urlpatterns = [
    path('ping/',views.ping,name='ping'),
    path('',views.main,name='main'),
    path('search/', views.search_results_view, name='search_results'),
    path('law/<int:pk>/', views.law, name='law'),
    path('archive/', views.archive_view, name='archive'),
    path('Privacy_Policy/', views.Privacy_Policy, name='Privacy_Policy')
    
]