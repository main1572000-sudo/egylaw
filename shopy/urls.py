from django.urls import path
from . import views
urlpatterns = [
    path('ping/',views.ping,name='ping'),
    path('',views.main,name='main'),
    path('search/', views.search_results_view, name='search_results'),
    path('law/<int:pk>/<slug:slug>/', views.law, name='law'),
    path('archive/', views.archive_view, name='archive'),
    path('Privacy_Policy/', views.Privacy_Policy, name='Privacy_Policy'),
    path('contact_Us/', views.Contact_Us, name='Contact_Us'),
    path('About_Us/', views.About_Us, name='About_Us'),
    path('consult/', views.Consult, name='consult'),
    path('Terms_And_Conditions/', views.Terms_and_Conditions, name='Terms_And_Conditions'),
    
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('dashboard/users/', views.users_list, name='users_list'),
    path('dashboard/users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('dashboard/users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/topics/',views.Topics,name='topics'),
    
    path('dashboard/topics/new_topic/',views.Add_Topic,name='new_topic'),
    path('dashboard/topics/delete_topic/<int:topic_id>/',views.Delete_Topic,name='delete_topic'),
    path('dashboard/topics/edit_topic/<int:pk>/',views.Edit_Topic,name='edit_topic'),
    ]