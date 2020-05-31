from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from tour.choices import *

class Profile(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  birthdate = models.DateField(null=True, blank=True)
  gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True,
   default=1)
  phone_number = models.CharField(validators=[phone_regex], max_length=10,
   blank=True)
  country = models.CharField(max_length=100, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Destination(models.Model):
  location_from = models.CharField(max_length=100, blank=True)
  location_to = models.CharField(max_length=100, blank=True)
  area = models.CharField(max_length=100, blank=True)
  destination_name = models.CharField(max_length=70, blank=True)

class Tour(models.Model):

  destination = models.OneToOneField(
    Destination,
    on_delete=models.CASCADE,
    primary_key=True,
  )
  tour_name = models.CharField(max_length=80, null=True, blank=True)
  experience_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
  price = models.DecimalField(max_digits=10, decimal_places=2)
  start_day = models.DateField(null=True, blank=True)
  end_day = models.DateField(null=True, blank=True)
  min_age = models.PositiveIntegerField(validators=[MinValueValidator(2)])
  max_people = models.IntegerField(validators=[MinValueValidator(1)])
  status_evaluete = models.IntegerField(choices=STATUS_E_CHOICES, default=0)
  detail_tour = models.TextField()

class Booking(models.Model):

  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
  status_booking = models.IntegerField(choices=STATUS_B_CHOICES, default=0)
  booking_time = models.DateField(auto_now_add=True)
  people_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])

class Photo(models.Model):
  tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='images/')

class Slider(models.Model):
  slider_image = models.ImageField(upload_to='images/', blank=True)
  title = models.CharField(max_length=100)
  teaser = models.TextField('teaser', blank=True)