from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from .forms import CardForm
from movies.models import Movie
from halls.models import Showtime
from .models import Ticket, Order, ShoppingCart, CardDetail
from .create_ticket_image import ticket_info, generate_ticket
import os
import payment
# adjust discount for each type here.
from advanced_booking import settings

ticket_value = {'CHILD': 5, 'ADULT': 5, 'SENIOR': 5 * 0.8}  # map ticket type to ticket values


def create_new_ticket(seat_id, showtime_id, ticket_type):
    """
    create a ticket
    """
    if seat_id and showtime_id and ticket_type:
        # create a new ticket
        # print("ticket_type is:")
        # print(ticket_type)
        new_ticket = Ticket.objects.create(seat_id=seat_id, showtime_id=showtime_id, type=ticket_type)
        return new_ticket


# cart functions  #
def add_to_cart(request, seat_id, showtime_id, ticket_type):
    """
    create a ticket and add it to user's shopping cart.
    If current user doesn't have cart, create it first and add ticket to it.

    return to the cart page
    """

    if request.user.is_authenticated:
        if seat_id and showtime_id and ticket_type:
            # create a new ticket
            # print("ticket_type is:")
            # print(ticket_type)
            # FIXME: elegant way to limit this.
            # Limit buying child ticket for movies which are 18 OR R18 in certificate.
            if ticket_type == 'CHILD':
                if Showtime.objects.get(id=showtime_id).movie.certificate in ["18", "R18"]:
                    messages.error(request, "Movie certificate Limitation:"
                                            " can't buy for child")
                    print("Error:Movie Rating Limitation")
                    return redirect('index')

            new_ticket = create_new_ticket(seat_id, showtime_id, ticket_type)
            if ShoppingCart.objects.filter(user=request.user).first():
                cart = ShoppingCart.objects.get(user=request.user)
                cart.ticket.add(new_ticket)
            else:
                cart = ShoppingCart.objects.create(user=request.user)
                cart.ticket.add(new_ticket)
            cart.save()
            return redirect('cart')
        else:
            messages.error(request, "Can't create ticket"
                                    " due to null values")
            print("Error: Can't create ticket due to null values")
            return redirect('index')
    else:
        messages.error(request, "Unauthenticated user!")
        print("Error: Unauthenticated user!")
        return redirect('index')


##cart view ###
def remove_from_cart(request, ticket_id):
    if request.user.is_authenticated:
        current_user = request.user
        # query the cart
        cart = ShoppingCart.objects.get(user=current_user)
        ticket = Ticket.objects.get(id=ticket_id)
        cart.ticket.remove(ticket)
        cart.save()
        return redirect('cart')
    else:
        messages.error(request, "failed to remove ticket from cart")
        print("Error: failed to remove ticket from cart")
        return redirect('index')


def cart(request):
    # handle some messages from failed booking
    messages.get_messages(request)
    if request.user.is_authenticated:
        current_user = request.user

        # query the cart
        try:
            cart = ShoppingCart.objects.get(user=current_user)
        except:
            cart = ShoppingCart.objects.create(user=request.user)

        cart = ShoppingCart.objects.get(user=current_user)

        # FIXME: if front-end just want tickets in the cart, do:
        tickets = cart.ticket.all()

        amount = sum(ticket_value[ticket.type] for ticket in tickets)

        context = {
            "cart": cart,
            "tickets": tickets,
            "amount": amount
        }
        return render(request, 'payment/cart.html', context)
        # add ticket to context
    else:
        messages.error("Need login!")
        return redirect('index')


def book_ticket(user, card):
    """
    Creates a booking for the user with the card. It marks the seat
    as reserved and removes the shopping cart object.

    Return True if booked successful, else return False
    """
    cart = ShoppingCart.objects.get(user=user)

    tickets = cart.ticket.all()

    trigger = 0  # inital trigger
    for ticket in tickets:
        if ticket.seat.status == 'X':  # any ticket has been booked
            cart.ticket.remove(ticket)
            trigger = 1  # any removed ticket triggered failed to book

    if trigger:
        return False

    amount = sum(ticket_value[ticket.type] for ticket in tickets)
    order = Order.objects.create(
        user=user,
        card=card.__str__(),
        order_status='Succeed',
        amount=amount
    )

    for ticket in tickets:
        order.tickets.add(ticket)
        ticket.seat.status = 'X'  # Marking seat as booked
        ticket.seat.save()
        ticket.save()
        # generate tickets
        generate_ticket(ticket_info(ticket))

    cart.delete()

    return True


def sendticket(order):
    """
    Send ticket to user
    """

    try:
        subject = "Your order" + str(order.id) + "(Digital ticketed included)"
        mail = EmailMessage(subject,
                            'Thank you for booking with us.',
                            settings.EMAIL_HOST_USER,
                            [order.user.mail])
        path = os.path.dirname(payment.__file__)

        for ticket in order.tickets.all():
            mail.attach_file(f'{path}/resources/rendered_tickets/ticket{ticket.id}.pdf')
        mail.send()
        print("Success: Sent tickets to useremail.")
    except:
        print('Error: Failed to send email: CAN NOT attach files')  ## big or corrupt


def checkout(request):
    """
    this view is rendering "checkout" page with forms
    """
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid:
            card = form.save()
            if book_ticket(request.user, card) == False:
                messages.error(request, 'Some tickets are unavailable. Please try again.')
                return redirect('cart')

            messages.success(request, 'Successfully booked tickets. Check email for your tickets. ')
            return redirect('booking')
    else:
        form = CardForm()
        context = {
            'form': form,
            'buttonText': "Pay",
            'action': "",
            'title': "Checkout"
        }
        return render(request, 'payment/payment.html', context)
