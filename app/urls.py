from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home & Products
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.detail, name='detail'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # Django built-in password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Profile & Orders
    path('account/', views.account_view, name='account'),
    path('account/update/', views.update_profile, name='update_profile'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # Order Success
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # Checkout/Buy Now
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),

    # Payment
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('contact/', views.contact_view, name='contact'),

]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
