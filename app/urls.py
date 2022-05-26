
from  django.urls import path
from .views import CategoryView, CheckOutView, CreatePayment, Detail, Home, OrderFinish, OrderSummaryView, PaymentView, SearchView, add_to_cart, remove_from_cart, remove_single_item_from_cart

app_name = 'app'
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('detail/<slug>/',Detail.as_view(),name='detail'),
    path('add_to_cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('summary/',OrderSummaryView.as_view(),name='summary'),
    path('remove/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('remove_single/<slug>/',remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('checkout/',CheckOutView.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name='payment'),
    path('create_payment/',CreatePayment,name='create-payment'),
    # path('endpoint/',webhook,name='webhook'),
    path('order_finish/',OrderFinish,name='order-finish'),
    path('category/<str:category>/',CategoryView.as_view(),name='category'),
    path('search/',SearchView.as_view(),name='search'),
]

