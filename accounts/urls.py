from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('logout/',logout, name="logout"),
   path('aboutus/', about_us, name="about_us"),
   path('register/' , register_page , name="register"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('cart/' , cart , name="cart"),
   path('add-to-cart/<uid>/' , add_to_cart, name = "add_to_cart"),
   path('search/' , search , name = "search"),
   path('order_history/', order_history, name='order_history'),
   # path('rate_product', rate_product, name='rate_product'),
   path('rate_website', rate_website, name='rate_website'),
   path('view_ratings/', view_ratings, name='view_ratings'),
   path('compare/', compare_products, name='compare_products'),    
   

   path('remove-cart/<cart_item_uid>' , remove_cart , name = "remove_cart"),
   path('remove-coupon/<cart_id>/' , remove_coupon , name = "remove_coupon"),
   path('success/' , success , name = "success"),
   path('user-details/', user_details, name='user_details'),
   path('order_history/', order_history, name='order_history'),
   path('contact-us/', contact_us, name='contact_us'),
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   path('generate_bill/<str:order_id>/<str:payment_id>/', generate_bill, name='generate_bill'),


]