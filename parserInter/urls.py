from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('personal/', PersonalView.as_view(), name='personal'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='product-update'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('product-in-order/<int:pk>/', ProductInOrderUpdateView.as_view(), name='product-in-order-update'),

    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/delete/<int:pk>', OrderDeleteView.as_view(), name='order-delete'),
    path('delete/from/order/<int:pk>', DeleteFromOrderView.as_view(), name='delete-from-order'),
    path('repeat/order/<int:pk>', RepeatOrderView.as_view(), name='repeat-order'),

    path('cart/', CartView.as_view(), name='cart'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('send/email/', send_email, name='send-email'),
    path('send/order/', send_order, name='send-order'),

    path("login/", Login.as_view(), name="login"),
]
