from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *

from tour.forms import SignUpForm, BookingForm

# Register
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.country = form.cleaned_data.get('country')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.info(request,'Your account has been created')
            return redirect('index')
    else:
        form = SignUpForm()

    context={
        'form':form
    }
    return render(request, 'registration/signup.html', context)

def index(request):
    destinations = Area.objects.prefetch_related('areas', 'areas__tours').annotate(num_tour=Count('areas__tours'))[:6]
    sliders = Slider.objects.all()
    # places = Tour.objects.select_related('destination').prefetch_related('tour_photo','review_set').annotate(num_review=Count('review'))[:6]
    blogs = Blog.objects.select_related('user')[:3]

    context = {
        'destinations' : destinations,
        'sliders' : sliders,
        'places' : Tour.get_tour_list,
        'blogs' : blogs,
    }

    return render(request, 'index.html', context)

def  about(request):
    done_bookings = Booking.objects.filter(status_booking=1)
    tour_totals = Tour.objects.count()
    clients = User.objects.count()
    blogs = Blog.objects.select_related('user')[:3]
    context = {
        'bookings' : done_bookings.count,
        'tour_totals' : tour_totals,
        'clients' : clients,
        'blogs' : blogs,
    }

    return render(request, 'about.html', context)

def pagination(request,self):
    page = request.GET.get('page', 1)
    paginator = Paginator(self, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result

def destination(request):
    places = pagination(request,Tour.get_tour_list())
    blogs = Blog.objects.select_related('user')[:3]
    context = {
        'places' : places,
        'blogs' : blogs
    }
    return render(request, 'destination.html', context)


def destination_detail(request,pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BookingForm(request.POST, author=request.user, tour=tour)
            if form.is_valid():
                booking = form.save();
                return redirect('index')
            else:
                return redirect('destination_detail', pk=pk)
        else:
            return redirect('login')
    else:
        form = BookingForm()

    context = {
        'tour' : tour,
        'form':form
    }
    return render(request, 'destination_detail.html', context)
def contact(request):
    return render(request, 'contact.html')
