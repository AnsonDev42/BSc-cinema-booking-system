from datetime import date, datetime, timezone
from django.urls import reverse
from django.test import TestCase, SimpleTestCase
from .models import Movie
from halls.models import Showtime, Hall


def create_hall():
    """
    Create a new hall
    """
    return Hall.objects.create(
        name="screen1"
    )


def create_movie(title):
    """
    Create a new movie with the given title.
    """
    return Movie.objects.create(
        title=title,
        director='John Doe',
        lead_actor='Person 1, Person 2, Person 3',
        certificate='PG',
        duration=199,
        rating=5.1,
        premier_date=date(2020, 1, 1)
    )


def create_showtime(hall, movie, showtime):
    """
    Create a new showtime with the given hall and movie.
    """
    return Showtime.objects.create(
        hall=hall,
        movie=movie,
        time=showtime
    )


class MovieViewTests(TestCase):
    def test_movie_empty_index_page(self):
        """
        The movie index page should not be displaying any movies.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['movie_list'], [])

    def test_movie_index_page(self):
        """
        The movie index page should display the movies.
        """
        for i in range(3):
            create_movie(f'Title of Movie {i + 1}')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        for i in range(3):
            self.assertContains(response, f'Title of Movie {i + 1}')

        self.assertEqual(len(response.context['movie_list']), 3)

    def test_movie_info_page(self):
        """
         a movie info page should be able to access in every situation
         (if can't query fallback to index page)
        """
        for i in range(3):
            create_movie(f'Title of Movie {i + 1}')

        response = self.client.get(reverse('movie', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Title of Movie {2}')
        self.assertNotContains(response, f'Title of Movie {1}')

        response = self.client.get(reverse('movie', args=[10]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Title of Movie {1}')

    def test_seat_form(self):
        """
        this tests if the seat page can be rendered
        """
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )

        response = self.client.get(reverse('seat', args=[show.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'seat')

        # TODO: write a test that can check if the route is correct



