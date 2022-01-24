from django.urls import path
from .views import *

urlpatterns = [
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),
         name='order-confirmation'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
]
