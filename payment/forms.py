from django import forms
from django.forms import ModelForm

from movies.models import Movie
from halls.models import Showtime, Seat
from .models import CardDetail


class CardForm(ModelForm):
    """Simple card form to create new card"""
    save_card = forms.BooleanField(required=False)
    # TODO add validations

    def save(self, commit=True):
        """
        Overriding the default save method. If user allows the 
        card to be stored in the database then only save it.
        """
        card = super().save(commit=False)
        if commit and self.cleaned_data['save_card']:
            card.save()
        return card

    class Meta:
        model = CardDetail
        fields = ['card_number', 'card_holder_name',
                  'expire_month', 'expire_year', 'save_card']


class SelectDatetimeForm(forms.Form):
    """
    This form provides a datetime choice field for a ticket
    """

    def __init__(self, *args, **kwargs):
        movie_id = kwargs.pop('movie_id', None)
        super(SelectDatetimeForm, self).__init__(*args, **kwargs)

        # use movie_id to query available_datetime
        if movie_id:
            available_datetime = Showtime.objects.all().filter(movie_id=movie_id)
            self.fields['selected_showtime'] = forms.ChoiceField(
                choices=tuple([(a_time.id, a_time) for a_time in available_datetime]))


class SelectSeatForm(forms.Form):
    """
    This form provides a SEAT choice field and a AGE choice field for a ticket
    """

    def __init__(self, *args, **kwargs):
        showtime_id = kwargs.pop('showtime_id', None)
        super(SelectSeatForm, self).__init__(*args, **kwargs)

        # use showtime to grab all available seats
        if showtime_id:
            available_seats = Seat.objects.all().filter(showtime_id=showtime_id)
            self.fields['selected_seats'] = forms.ChoiceField(
                choices=tuple([(a_seat.id, a_seat) for a_seat in available_seats]))

    # add
    AGE_CHOICES = (
        ("CHILD", "Child(Under 16)"),
        ("ADULT", "Adult(17-64)"),
        ("SENIOR", "Senior(Over 65)"),
    )

    ticket_type = forms.ChoiceField(choices=AGE_CHOICES)
