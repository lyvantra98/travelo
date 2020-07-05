from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm

from tour.choices import *
from .models import *

class SignUpForm(UserCreationForm):

  gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Giới tính", initial='',
   widget=forms.Select(), required=True)
  phone_number = forms.CharField(validators=[phone_regex], max_length=10, label="Điện thoại")
  country = forms.CharField(max_length=100, label="Thành phố")
  first_name = forms.CharField(label="Họ")
  last_name = forms.CharField(label="Tên")
  email = forms.CharField(label="Địa chỉ email")
  password1 = forms.CharField(label="Mật khẩu")
  password2 = forms.CharField(label="Xác nhận mật khẩu")
  username = forms.CharField(label="Tên đăng nhập")
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

class BookingForm(forms.ModelForm):
  people_number = forms.IntegerField(widget=forms.TextInput(
      attrs={'placeholder':'Số người','type':'number','min':'1'}))

  def __init__(self, *args, **kwargs):
    query = kwargs.pop('max_people', None)

    super(BookingForm, self).__init__(*args, **kwargs)

    self.fields['people_number'].widget.attrs['max']= query

  class Meta:
    model = Booking
    fields = ('people_number',)

class CommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':20, 'class':'form-control ml-1 shadow-none textarea'}))

  class Meta:
    model = Review
    fields = ('content',)

class BlogForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(attrs={'rows':9, 'cols':30, 'class':'form-control w-100', 'placeholder':'Nội dung'}))
  title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tiêu đề'}))
  tag = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tag'}))
  image = forms.ImageField()

  class Meta:
    model = Blog
    fields = ('content', 'title', 'tag', 'image',)

class Editprofile(UserCreationForm):
  gender = forms.ChoiceField(choices=GENDER_CHOICES, label='', initial='',
   widget=forms.Select(), required=True)
  email = forms.CharField(label='')
  phone_number = forms.CharField(validators=[phone_regex], max_length=10, label='')
  country = forms.CharField(max_length=100, label='')
  birthday = forms.DateField(label='', widget=forms.DateInput(attrs={'type' : 'date'}))
  first_name = forms.CharField(label='')
  last_name = forms.CharField(label='')
  image = forms.ImageField()

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
        raise ValidationError('Tài khoản với email đó đã tồn tại')
    return email

  def clean_phone_number(self):
    phone = self.cleaned_data['phone_number']
    if Profile.objects.filter(phone_number=phone).exists():
        raise ValidationError('Tài khoản với số điện thoại đã tồn tại')
    return phone

  def __init__(self, *args, **kwargs):
    birthday = kwargs.pop('birthday', None)
    email = kwargs.pop('email', None)
    country = kwargs.pop('country', None)
    first_name = kwargs.pop('first_name', None)
    last_name = kwargs.pop('last_name', None)
    phone = kwargs.pop('phone', None)
    gender = kwargs.pop('gender', None)
    image = kwargs.pop('image', None)
    super(Editprofile, self).__init__(*args, **kwargs)
    self.fields['birthday'].widget.attrs['value']= birthday
    self.fields['email'].widget.attrs['value']= email
    self.fields['country'].widget.attrs['value']= country
    self.fields['first_name'].widget.attrs['value']= first_name
    self.fields['last_name'].widget.attrs['value']= last_name
    self.fields['phone_number'].widget.attrs['value']= phone
    self.fields['gender'].widget.attrs['value']= gender
    self.fields['image'].widget.attrs['value']= image

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'country', )

class Tour(forms.ModelForm):

  class Meta:
    models = Tour
    fields = ('tour_name', 'image')

