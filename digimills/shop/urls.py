from shop.forms import LoginForm, UserPasswordChangeForm, UserPasswordResetForm,UserSetNewPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import REDIRECT_FIELD_NAME, views as auth_views
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about/', views.about, name="about"),
    path('accounts/address/', views.ShowAddressView.as_view(), name="show_address"),
    path('account_edit/<slug:username>/', views.AccountEditView.as_view(), name="account_edit"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    
    path('cart/', views.show_cart, name="cart"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('order/', views.order, name="orders"),
    
    path('checkout/', views.checkout, name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),

    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),
   
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html', form_class=LoginForm, redirect_field_name='account'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='shop/password_change.html', form_class=UserPasswordChangeForm) , name="password_change"),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="shop/password_change_done.html"), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=UserPasswordResetForm), name="password_reset"),
    path('aaccounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html', form_class=UserSetNewPasswordForm), name="password_reset_confirm"),
    path('accounts/password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name="password_reset_done"),
    path('accounts/reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html',), name="password_reset_complete"),

    path('mobile/', views.MobileView.as_view(), name="mobile"),
    path('mobile/<slug:brand>', views.MobileView.as_view(), name="mobile"),
    path('privacy/', views.privacy, name="privacy"),
    path('product_single/<int:pk>/', views.ProductSingleView.as_view(), name="product_single"),
    path('products/', views.ProductsView.as_view(), name="products"),
    # path('products/<slug:categ>/', views.ProductsView.as_view(), name="products_categ"),
    path('register/', views.UserRegister.as_view(), name="register"),
    path('terms/', views.terms, name="terms"),
    path('user_detail/<int:pk>', views.terms, name="user_details"),
]
