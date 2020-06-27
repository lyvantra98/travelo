from django.urls import path, include

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('destination/', views.destination, name='destination'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('contact/', views.contact, name='contact'),
]
