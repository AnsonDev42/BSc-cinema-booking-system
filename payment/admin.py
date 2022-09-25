from django.contrib import admin

from .models import ShoppingCart, Ticket, CardDetail, Order
from movies.models import Movie
from halls.models import Hall, Seat, Showtime


# Register your models here.
class TicketInterface(admin.ModelAdmin):
    list_display = ('__str__', 'showtime', 'seat', 'type')
    search_fields = ['type', 'seat', 'showtime']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CardDetailInterface(admin.ModelAdmin):
    list_display = ('__str__', 'card_holder_name')
    search_fields = ['user', 'card_holder_name']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class OrderInterface(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'card', 'get_tickets', 'order_status', 'amount', 'date_created')
    search_fields = ['user', 'tickets']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    # print all tickets in list_display
    def get_tickets(self, obj):
        return ", ".join([str(p) for p in obj.tickets.all()])


class ShoppingCartInterface(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'ticket')
    search_fields = ['user', 'tickets']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Ticket, TicketInterface)
admin.site.register(CardDetail, CardDetailInterface)
admin.site.register(Order, OrderInterface)
admin.site.register(ShoppingCart)
