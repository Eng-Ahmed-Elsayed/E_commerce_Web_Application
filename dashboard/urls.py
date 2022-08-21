from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashHome, name='dashboard'),
    path('favorite_ads/', views.favoriteAds, name='favorite_ads'),
    path('pending_approval/', views.pendingApproval, name='pending_approval'),
    path('archived_ads/', views.archivedAds, name='archived_ads'),
    path('ad_list/', views.adList, name='ad_list'),
    path('ad_view/<str:pk>/', views.adView, name='ad_view'),
    path('edit_ad/<str:pk>/', views.editAd, name='edit_ad'),
    path('delete_ad/<str:pk>/', views.deleteAd, name='delete_ad'),
    path('delete_ad_from_fav/<str:pk>/', views.deleteAdFromFav, name='delete_ad_from_fav'),
    path('add_ad_to_fav/<str:pk>/', views.addAdToFav, name='add_ad_to_fav'),
    path('edit_review/<str:pk>/', views.editReview, name='edit_review'),
    path('delete_review/<str:pk>/', views.deleteReview, name='delete_review'),



]

    
