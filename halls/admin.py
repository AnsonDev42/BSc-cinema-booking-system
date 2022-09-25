from django.contrib import admin

from .models import Hall, Seat, Showtime


class HallInterface(admin.ModelAdmin):
    # FIXME: the problem is that Django admin site cannot recognise
    #        the relationship between halls and seats even if the
    #        the relationship is well defined.
    pass


class SeatInterface(admin.ModelAdmin):
    list_display = ('__str__', 'hall', 'showtime', 'row_number', 'seat_number', 'vip', 'status')
    search_fields = ['hall__name', 'row_number', 'seat_number']
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ShowtimeInterface(admin.ModelAdmin):
    list_display = ('__str__', 'movie', 'hall', 'time')
    search_fields = ['movie__title', 'hall__name', 'time']
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Showtime, ShowtimeInterface)
admin.site.register(Hall)
admin.site.register(Seat, SeatInterface)
