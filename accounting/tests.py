import datetime
from django.test import TestCase
from users.tests import create_user
from payment.models import Order
from .views import get_income_between


class AccountingTest(TestCase):
    def setUp(self):
        # Create user
        user = create_user('user1@user1.com', 'user1', 'aa8oeAWDaVA')
        # Create multiple bookings
        for i in range(1, 10):
            o = Order.objects.create(
                user=user,
                card='90328410983094',
                order_status='Succeed',
                amount=5 * i,
            )
            o.date_created = datetime.datetime(2021, 2, i, 0, 0, 0)
            o.save()

    def test_get_income_between(self):
        # Create another order on a day
        o = Order.objects.create(
            card='90328410983094',
            order_status='Succeed',
            amount=20,
        )
        o.date_created = datetime.datetime(2021, 2, 3, 0, 0, 0)
        o.save()

        start_date = datetime.datetime(2021, 1, 31, 0, 0, 0)
        end_date = datetime.datetime(2021, 2, 6, 0, 0, 0)

        data = get_income_between(start_date, end_date)
        # Test size of data
        self.assertEqual(len(data), 7)

        # Test for date created for each array
        self.assertEqual(data[0][0], '31-01-2021')
        self.assertEqual(data[1][0], '01-02-2021')
        self.assertEqual(data[2][0], '02-02-2021')
        self.assertEqual(data[3][0], '03-02-2021')
        self.assertEqual(data[4][0], '04-02-2021')
        self.assertEqual(data[5][0], '05-02-2021')
        self.assertEqual(data[6][0], '06-02-2021')

        # Test for sum of amount is the same
        self.assertEqual(data[0][1], 0)
        self.assertEqual(data[1][1], 5)
        self.assertEqual(data[2][1], 10)
        self.assertEqual(data[3][1], 35)
        self.assertEqual(data[4][1], 20)
        self.assertEqual(data[5][1], 25)
        self.assertEqual(data[6][1], 30)
