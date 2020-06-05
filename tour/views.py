from django.shortcuts import render, redirect
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate

from .models import *

from tour.forms import SignUpForm

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

#Login "Email Or Username" processing
class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def index(request):
    # destinations = Destination.objects.values('area').annotate(Count('tour'))[:6]
    sliders = Slider.objects.all()
    # places = Tour.objects.select_related('destination')[:6]
     # reviews_number = Review.objects.values(tour=places.).annotate(Count('id'))
    context = {
        'destinations' : destinations,
        'sliders' : sliders,
        'places' : places,
        # 'reviews_number' : reviews_number,
    }

    return render(request, 'index.html', context)

