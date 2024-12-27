from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path("product/", product, name='product'),
    path("search/", search, name='search'),
    path("products/<int:id>/", product_detail, name='product_detail'),
    path("contact/", contact, name='contact'),
    path("about/", about, name='about'),
    path("account/", account, name='account'),
    path("compare/",compare,name='compare'),
    
    
    
    # for authentication
    path("register/", register, name='register'),
    path("login/", log_in, name="log_in"),
    path("logout/", log_out, name='log_out'),
    
    #for sidebar:
    path("blog_single_left/",blog_single_left,name='blog_single_left'),
    path("blog_single_right/",blog_single_right,name='blog_single_right'),
    path('single_product/<int:id>/', single_product, name='single_product'),
    path("shop_left_sidebar/",shop_left_sidebar,name='shop_left_sidebar'),
    
    # for cart
    path("cart/", cart_detail, name='cart_detail'),
    path("checkout/",checkout,name="checkout"),
    path("success/",success, name='success'),
    path("placeorder/",place_order,name="place_order"),
    path("yourorder/",your_order,name='your_order'),
    path("payment/",payment,name='payment'),
    #path("single_product/",single_product,name='single_product'),
    
    # cart actions
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    
    
    #for forget Password:
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete'), name='password_reset_complete'),

    
]
