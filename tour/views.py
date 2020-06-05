from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db.models import Count

from .models import *

from tour.forms import SignUpForm

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
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def index(request):
    areas = Destination.objects.values('area').annotate(Count('tour'))
    sliders = Slider.objects.all()
    context = {
        'areas' : areas,
        'sliders' : sliders,
    }

    return render(request, 'index.html', context)

