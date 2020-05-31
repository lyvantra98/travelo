from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from tour.choices import *
from .models import *

class SignUpForm(UserCreationForm):
  gender = forms.ChoiceField(choices=GENDER_CHOICES, label="", initial='',
   widget=forms.Select(), required=True)
  phone_number = forms.CharField(validators=[phone_regex], max_length=10)
  country = forms.CharField(max_length=100)

  class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email', 'gender',
       'password1', 'password2', )

class Tour(forms.ModelForm):

  class Meta:
    models = Tour
    fields = ['tour_name', 'image']

