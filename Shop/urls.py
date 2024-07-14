from django.urls import path
from .views import home_view, register_view,cart_view,add_to_cart,CheckoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
      path('', auth_views.LoginView.as_view(template_name='login.html')),
      path('logout/', auth_views.LogoutView.as_view(template_name='logout.html')),
    path('register/', register_view,name='register'),
   path('home/',home_view,name='home'),
   path('home/cart/',cart_view,name="cart"),
  path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
  path('CheckoutView', CheckoutView, name='CheckoutView'),
]
