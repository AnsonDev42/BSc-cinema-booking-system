from datetime import date, datetime, timezone, tzinfo
from django.test import TestCase

from .models import Hall, Showtime, Seat
from movies.models import Movie


class ShowtimeTest(TestCase):
    def test_seat_generation(self):
        hall = Hall.objects.create(name='Hall 1')
        movie = Movie.objects.create(
            title='Movie 1',
            director='Director 1, Director 2, Director 3',
            lead_actor='Actor 1, Actor 2, Actor 3',
            certificate='PG',
            duration=100,
            rating=5.0,
            premier_date=date(2021, 2, 5),
            blurb="Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa, mollitia?"
        )
        time = datetime(2021, 2, 5, 12, 0, 0, 0, timezone.utc)
        showtime = Showtime.objects.create(
            hall=hall,
            movie=movie,
            time=time
        )
        showtime.save()
        all_seats = Seat.objects.filter(showtime=showtime)
        for seat in all_seats:
            self.assertEqual(seat.showtime.time, time)
            self.assertEqual(seat.hall, hall)
            self.assertEqual(seat.status, 'O')
