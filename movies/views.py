from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from payment.forms import SelectDatetimeForm, SelectSeatForm
from .models import Movie
from halls.models import Showtime
from payment.views import add_to_cart
from payment.models import Order, ShoppingCart


def index(request):
    messages.get_messages(request)
    movie_list = Movie.objects.all()
    context = {
        'movie_list': movie_list,
    }
    return render(request, 'movies/index.html', context)


def movie(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except:
        return index(request)

    context = {
        'movie': movie,
    }

    if request.method == 'POST':
        form = SelectDatetimeForm(request.POST, movie_id=movie_id)

        if form.is_valid():
            print("SelectDatetimeForm is valid")
            selected_showtime_id = form.cleaned_data['selected_showtime']
            return redirect('seat', selected_showtime_id)
        else:
            print(" Not a valid SelectDatetimeForm")
    else:
        # create a Datatime form for the current page movie
        form = SelectDatetimeForm(movie_id=1)
        # add form to conext
        context['form'] = form

    return render(request, 'movies/movie.html', context)


def seat(request, showtime_id):
    context = {

    }
    if showtime_id:
        showtime = Showtime.objects.get(pk=showtime_id)
        movie = showtime.movie
        hall = showtime.hall

        # TODO: add required info for front-end
        context['movie'] = movie
        context['hall'] = hall
        if request.method == 'POST':
            form = SelectSeatForm(request.POST, showtime_id=showtime_id)

            if form.is_valid():
                print("SelectSeatForm is valid")
                selected_seat_id = form.cleaned_data['selected_seats']
                ticket_type = form.cleaned_data['ticket_type']
                # add cart for login user
                if request.user.is_authenticated:
                    current_user = request.user
                    #create ticket and add to cart
                    print("successfully created a ticket and added to cart")
                    return redirect(add_to_cart, seat_id=selected_seat_id, showtime_id=showtime_id,
                                    ticket_type= ticket_type)

                else:
                    print("Error: form not valid!")
                    return redirect('index')
            else:
                print(" Not a valid SelectDatetimeForm")
        else:
            # create a Datatime form for the current page movie
            form = SelectSeatForm(showtime_id=showtime_id)
            # add form to conext
            context['form'] = form

    return render(request, 'movies/seat.html', context)
