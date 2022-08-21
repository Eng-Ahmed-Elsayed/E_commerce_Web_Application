from django.urls import path
from . import views


urlpatterns = [
    path('', views.myCart, name='my_cart'),
    path('my_purchases', views.myPurchases, name='my_purchases'),
    path('add_to_cart/<str:pk>/', views.addToCart, name='add_to_cart'),
    path('delete_from_cart/<str:pk>/', views.deleteFromCart, name='delete_from_cart'),
    path('buy_ad/<str:pk>/', views.buyAd, name='buy_ad'),
    path('paypal/<str:pk>/', views.paypal, name='paypal'),

]

    
