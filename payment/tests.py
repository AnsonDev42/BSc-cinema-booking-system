from datetime import date, datetime, timezone
import random
from django.urls import reverse
from django.test import TestCase, SimpleTestCase
from movies.models import Movie
from halls.models import Showtime, Hall, Seat
from .models import CardDetail, ShoppingCart, Ticket, Order
from users.models import User

from users.tests import create_user
from movies.tests import create_hall, create_movie, create_showtime

from .views import book_ticket, create_new_ticket, add_to_cart, remove_from_cart
from .create_ticket_image import *


class MovieViewTests(TestCase):
    def test_create_ticket(self):
        """
        this is the test for create_new_ticket funciton
        to test if it can create a ticket correctly
        """
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )
        # created ticket has default type :adult
        ticket = Ticket.objects.create(seat_id=1, showtime=show)
        test_ticket = create_new_ticket(1, show.id, "ADULT")

        self.assertEqual(ticket.showtime, test_ticket.showtime)
        self.assertEqual(ticket.seat_id, test_ticket.seat_id)
        self.assertEqual(ticket.type, test_ticket.type)

    def test_ticket_to_string(self):
        # self.assertEqual(ticket.showtime, test_ticket.showtime)
        """
            test if the conversion function can convert string

        """
        # create a ticket for test
        show = create_showtime(
            create_hall(),
            create_movie(f'Title of Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )
        # created ticket has default type :adult
        ticket = Ticket.objects.create(seat_id=1, showtime=show)
        test_ticket = create_new_ticket(1, show.id, "ADULT")

        self.assertEqual("Title of Movie 1", ticket_info(test_ticket)["title"])
        self.assertEqual("PG", ticket_info(test_ticket)["certificate"])
        self.assertEqual("01/01/2021", ticket_info(test_ticket)["date"])  # since it formats as m/d/Y
        self.assertEqual("12:00", ticket_info(test_ticket)["time"])  # since it formats as %H:%M
        self.assertEqual("screen1", ticket_info(test_ticket)["screen"])
        self.assertEqual("ADULT", ticket_info(test_ticket)["ticket_type"])
        self.assertEqual("1", ticket_info(test_ticket)["seat_row"])
        self.assertEqual("1", ticket_info(test_ticket)["seat_number"])
        self.assertEqual("2", ticket_info(test_ticket)["ticket_id"])

        # if the create_ticket_image works, it should pop the image for you

        # generate_ticket(ticket_info(test_ticket))

        # FIXME: write tests to support "function+view" functions
    # see Issue #33 in Gitlab
    # def test_add_to_cart(self):
    #     show = create_showtime(
    #         create_hall(),
    #         create_movie(f'Title of Movie 1'),
    #         datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
    #     )
    #
    #     create_user('123@test.com', 'test_user1', 'qwe@123')
    #     test_user = User.objects.get(id=1)
    #     result = add_to_cart(request=test_user, seat_id=1, showtime_id=show.id, ticket_type="Adult")
    #     # test adding function
    #     self.assertContains(result, "cart")
    #     # test query back
    #     cart = ShoppingCart.objects.get(user=User.objects.get(id=1))
    #     self.assertNotEqual(cart, None)
    #     self.assertEqual(cart.ticket.first().id, 1)

    # FIXED: write test for removing view
    # def test_remove_ticket(self):
    #     show = create_showtime(
    #         create_hall(),
    #         create_movie(f'Title of Movie 1'),
    #         datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
    #     )
    #
    #     create_user('123@test.com', 'test_user1', 'qwe@123')
    #     test_user = User.objects.get(id=1)
    #     is_logged_in = self.client.login(
    #         email='123@test.com', password='qwe@123')
    #

    #     # request = None
    #     # request.user = test_user
    #     # response = add_to_cart(request, seat_id=1, showtime_id=show.id, ticket_type="Adult")
    #     # self.assertContains(response,"cart")
    #     # cart = ShoppingCart.objects.get(user=User.objects.get(id=1))
    #     # self.assertEqual(cart.ticket.first().id, 1)
    #     # test_return = remove_from_cart(user=User.objects.get(id=1), ticket_id=1)
    #     # self.assertEqual(test_return, True)
    #     # self.assertEqual(cart.ticket.all().first(), None)
    #     # # test if it's removed


class BookingProcessTest(TestCase):
    def setUp(self):
        create_user('user1@user1.com', 'user1', 'Qzh6=?sx-!B-eeJ6')
        create_showtime(
            create_hall(),
            create_movie('Movie 1'),
            datetime(2021, 1, 1, 12, 0, 0, 0, timezone.utc)
        )

    def test_book_ticket(self):
        user = User.objects.get(pk=1)

        seats = [Seat.objects.get(pk=i) for i in range(1, 4)]
        showtime = Showtime.objects.get(pk=1)
        tickets = [create_new_ticket(seats[i].pk, showtime.pk, 'ADULT')
                   for i in range(3)]

        cart = ShoppingCart.objects.create(user=user)
        for i in range(3):
            cart.ticket.add(tickets[i].pk)

        card = CardDetail.objects.create(
            card_number='1234567890123456',
            card_holder_name='user1',
            expire_month='1',
            expire_year='2022'
        )
        card.user.add(user)
        book_ticket(user, card)
        cart = ShoppingCart.objects.all()
        self.assertQuerysetEqual([], cart)
        order = Order.objects.filter(user=user)
        for o in order:
            self.assertEqual(user, o.user)
            self.assertEqual('**** **** **** 3456', o.card)
            self.assertEqual('Succeed', o.order_status)
        for ticket in tickets:
            self.assertEqual(ticket.seat.status, 'X')
