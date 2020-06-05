from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from tour.choices import *
from .models import *

class SignUpForm(UserCreationForm):

  gender = forms.ChoiceField(choices=GENDER_CHOICES, label="", initial='',
   widget=forms.Select(), required=True)
  phone_number = forms.CharField(validators=[phone_regex], max_length=10)
  country = forms.CharField(max_length=100)

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'country',
     'password1', 'password2', )

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
        raise ValidationError('Account with that email already exists')
    return email

  def clean_phone_number(self):
    phone = self.cleaned_data['phone_number']
    if Profile.objects.filter(phone_number=phone).exists():
        raise ValidationError('Account with that phone already exists')
    return phone

class Tour(forms.ModelForm):

  class Meta:
    models = Tour
    fields = ['tour_name', 'image']

