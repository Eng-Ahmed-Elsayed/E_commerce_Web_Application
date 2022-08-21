from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('edit_profile/', views.editProfile, name='edit_profile'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('404/', views.errorPage, name='404'),
    path('ad_list_view/', views.adListView, name='ad_list_view'),
    path('category_view/', views.categoryView, name='category_view'),
   


]