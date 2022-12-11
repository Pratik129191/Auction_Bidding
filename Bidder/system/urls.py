from django.urls import path
from . import views

app_name = 'system'

urlpatterns = [
    path('', views.home, name='home'),
    path('marketplace/', views.auctions, name='auctions'),
    path('marketplace/<auction_id>/', views.auction_detail, name='auction-detail'),

    path('my-bids/', views.bid_summary, name='bid-summary'),
    path('confirm-bids/', views.confirm_bids, name='confirm-bids'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about')
]



