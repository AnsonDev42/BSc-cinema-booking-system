from halls.models import Showtime
from django.shortcuts import render
from datetime import date, timedelta, datetime
from django.utils import timezone
from movies.models import Movie
from payment.models import Order, Ticket


def get_income_between(start_date, end_date):
    """
    Queries the order table for orders within our given range. 
    (:param start_date to :param end_date)
    Formats the data into an array
    [
        [date string, amount],
        [date string, amount],
        , ...
    ]
    """
    # Create an array with all the days within our range
    current_date = start_date.date()
    dates = []
    while(current_date <= end_date.date()):
        dates.append([current_date, 0])
        current_date += timedelta(days=1)

    # Because the query would be today : 00:00:00 it would not get
    # todays things.
    midnight = end_date + timedelta(days=1) - timedelta(microseconds=1)
    order = Order.objects.filter(date_created__range=[start_date, end_date])

    # Creating array of dates from start date to end date
    for o in order:
        index = o.date_created.date() - start_date.date()
        dates[index.days][1] += o.amount

    # Formatting the data for JavaScript parsing
    data_format = []
    for d in dates:
        data_format.append([f'{d[0].strftime("%d-%m-%Y")}', d[1]])

    return data_format


def accounting(request):
    """
    Queries the database for the week's income.
    """
    all_orders = Order.objects.all()
    overall_income = 0
    for o in all_orders:
        overall_income += o.amount

    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')

        data = get_income_between(start_date, end_date)
        context = {
            'start_date': start_date.strftime("%d-%m-%Y"),
            'end_date': end_date.strftime("%d-%m-%Y"),
            'data': data,
            'len': range(len(data)),
            'overall_income': overall_income,
        }
        return render(request, 'accounting/chart.html', context)

    today = timezone.now()
    last_week = today - timedelta(days=7)
    data = get_income_between(last_week, today)

    context = {
        'start_date': last_week.strftime("%d-%m-%Y"),
        'end_date': today.strftime("%d-%m-%Y"),
        'data': data,
        'len': range(len(data)),
        'overall_income': overall_income,
    }

    return render(request, 'accounting/chart.html', context)


def movie_income(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie_showtime = Showtime.objects.filter(movie=movie)
    tickets = []
    for ms in movie_showtime:
        tickets.append(Ticket.objects.filter(showtime=ms.pk))
    n_child = 0
    n_adult = 0
    n_senior = 0
    revenue = 0
    for i in range(len(tickets)):
        for t in tickets[i]:
            revenue += t.price
            if t.type == "CHILD":
                n_child += 1
            elif t.type == "ADULT":
                n_adult += 1
            elif t.type == "SENIOR":
                n_senior += 1

    context = {
        'n_child': n_child,
        'n_adult': n_adult,
        'n_senior': n_senior,
        'revenue': revenue,
        'movie': movie
    }
    return render(request, 'accounting/movie_chart.html', context)
