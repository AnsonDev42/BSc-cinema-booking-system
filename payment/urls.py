from django.urls import path

from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('cart', views.cart, name='cart'),
    path('cart/add_ticket/seat<int:seat_id>/showtime<int:showtime_id>/type<str:ticket_type>',
         views.add_to_cart, name='add_to_cart'),
    path('cart/remove_ticket/ticket<int:ticket_id>',views.remove_from_cart, name = 'remove_from_cart')

]
