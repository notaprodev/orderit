from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/user/', views.customerRegister, name='register'),
    path('login/user/', views.userLogin, name='login'),
    path('login/restaurant/', views.restLogin, name='rlogin'),
    path('register/restaurant/', views.restRegister, name='rregister'),
    path('profile/restaurant/', views.restaurantProfile, name='rprofile'),
    path('profile/user/', views.customerProfile, name='profile'),
    path('user/create/', views.Signup, name='signup'),
    path('user/update/<int:id>/', views.updateCustomer, name='cupdate'),
    path('restaurant/create/', views.createRestaurant, name='rcreate'),
    path('restaurant/update/<int:id>/', views.updateRestaurant, name='rupdate'),
    path('restaurant/orderlist/', views.orderlist, name='orderlist'),
    path('restaurant/menu/', views.menuManipulation, name='mmenu'),
    path('logout/', views.Logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),

]
