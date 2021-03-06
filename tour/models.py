from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.db.models import Count
from django.template.defaultfilters import truncatechars

from tour.choices import *
import datetime
import calendar

GENDER_CHOICES = (
  (0, 'Male'), (1, 'Female')
)
STATUS_E_CHOICES = (
  (0, 'Do not'),
  (1, 'Done')
)
STATUS_B_CHOICES = (
  (0, 'Waiting'),
  (1, 'Done')
)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True,
   default=1)
  phone_number = models.CharField(validators=[phone_regex], max_length=10,
   blank=True)
  country = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='images/profile', null=True)

  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Area(models.Model):
  area_name = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='images/area')

  def __str__(self):
    return self.area_name

class Destination(models.Model):
  area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='areas')
  location_from = models.TextField(max_length=50, blank=True)
  location_to = models.TextField(max_length=50, blank=True)
  destination_name = models.CharField(max_length=70, blank=True)

  def  __str__(self):
    return self.destination_name

class Tour(models.Model):
  destination = models.ForeignKey(
    Destination,
    on_delete=models.CASCADE,
    related_name='tours'
  )
  tour_name = models.TextField(max_length=80, null=True, blank=True)
  experience_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
  price = models.DecimalField(max_digits=10, decimal_places=0)
  start_day = models.DateField(null=True, blank=True)
  end_day = models.DateField(null=True, blank=True)
  min_age = models.PositiveIntegerField(validators=[MinValueValidator(2)])
  max_people = models.IntegerField(validators=[MinValueValidator(1)])
  status_evaluete = models.IntegerField(choices=STATUS_E_CHOICES, default=0)
  detail_tour = models.TextField()
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.tour_name + str(self.id)

  @property
  def short_tour_detail(self):
    return truncatechars(self.detail_tour, 200)

  @property
  def short_tour_name(self):
    return truncatechars(self.tour_name, 100)

  def get_tour_list(num):
    return Tour.objects.select_related('destination').prefetch_related('tour_photo','review').annotate(num_review=Count('review'))[:num]

  def short_date_end_start(self):
    return self.start_day.strftime('%d %b') + ' - ' + self.end_day.strftime('%d %b')

class Booking(models.Model):
  profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
  tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
  status_booking = models.IntegerField(choices=STATUS_B_CHOICES, default=0)
  booking_time = models.DateField(auto_now_add=True)
  people_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
  total_price =  models.DecimalField(max_digits=10, decimal_places=0)

  def __str__(self):
    return self.profile.username + " " + self.tour.tour_name


class Photo(models.Model):
  tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_photo')
  image = models.ImageField(upload_to='images/tours')

class Slider(models.Model):
  slider_image = models.ImageField(upload_to='images/sliders', blank=True)
  title = models.CharField(max_length=100)
  teaser = models.TextField('teaser', blank=True)

  def __str__(self):
    return self.title

class Review(models.Model):
  tour= models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='review')
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  like = models.IntegerField(null=True)

  def __str__(self):
    return self.content

class Blog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=150)
  content = models.TextField()
  date = models.DateField(auto_now_add=True)
  tag = models.CharField(max_length=50)
  image = models.ImageField(upload_to='images/blogs/')

  @property
  def short_blog_title(self):
    return truncatechars(self.title, 60)

  @property
  def short_blog_content(self):
    return truncatechars(self.content, 200)

  def month_name(self):
    month_number = int(self.date.month)
    return calendar.month_name[month_number]

  def __str__(self):
    return self.title

