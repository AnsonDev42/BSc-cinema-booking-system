from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.contrib.auth import views
from django.template.loader import render_to_string

from .models import User
from payment.models import Order,Ticket
from .forms import RegisterForm
from django.core.mail import send_mail
import payment
import os


def verify_user(request, user):
    token = user.generate_auth_token()
    hostname = request.META['HTTP_HOST']
    link = f'{hostname}/verify/{token}'
    msg_html = render_to_string('users/verification.html', {'token': link})
    send_mail(
        subject=f'Account verification for {user.username}',
        message=f'{token}',
        from_email='from@example.com',
        recipient_list=[user.email],
        fail_silently=False,
        html_message=msg_html,
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            verify_user(request, user)
            return redirect('index')
        else:
            context = {
                'form': RegisterForm(),
                'error_message': form.errors.as_text()
            }
            return render(request, 'users/register.html', context)
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)


def booking(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_order = Order.objects.filter(user=current_user)
        context = {
            'user': current_user,
            'order': user_order
        }
        return render(request, 'users/booking.html', context)
    return redirect(reverse('login'))


def verify(request, auth_token):
    try:
        user = User.objects.get(auth_token=auth_token)
        user.verified = True
        user.save()
        return render(request, 'users/verified.html')
    except:
        return redirect('index')
