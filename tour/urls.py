from django.urls import path, include

from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('destination/', views.destination, name='destination'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('contact/', views.contact, name='contact'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>', views.blog_detail, name='blog_detail'),
    path('area/<int:pk>', views.destination_area, name='destination_area'),
]
