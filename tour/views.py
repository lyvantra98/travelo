from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http.response import JsonResponse
import datetime

from decimal import Decimal

from paypal.standard.forms import PayPalPaymentsForm
from weasyprint import HTML
import tempfile
import stripe

from .models import *

from tour.forms import SignUpForm, BookingForm, CommentForm, BlogForm, Editprofile
# Register
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
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
                messages.info(request,'Tài khoản của bạn đã được tạo')
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
    blogs = Blog.objects.select_related('user')[:3]
    context = {
        'destinations' : destinations,
        'sliders' : sliders,
        'places' : Tour.get_tour_list(6),
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
    places = pagination(request,Tour.get_tour_list(6))
    blogs = Blog.objects.select_related('user')[:3]
    context = {
        'places' : places,
        'blogs' : blogs
    }
    return render(request, 'destination.html', context)

def destination_detail(request,pk):
    tour = get_object_or_404(Tour.objects.prefetch_related('tour_photo', 'review'), pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'comment' in request.POST:
                formcmt = CommentForm(request.POST)
                if formcmt.is_valid():
                    review = formcmt.save(commit=False)
                    review.author = request.user
                    review.tour = tour
                    review.content = formcmt.cleaned_data.get('content')
                    review.save()
                    return redirect('destination_detail', pk=pk)
                else:
                    return redirect('destination_detail', pk=pk)
            if 'booking' in request.POST:
                form = BookingForm(request.POST)
                if form.is_valid():
                    booking = form.save(commit=False)
                    num_people = form.cleaned_data.get('people_number')
                    request.session['tour_id'] = pk
                    request.session['people_number'] = num_people
                    request.session['total_price'] = num_people*int(tour.price)
                    return redirect('order')
                else:
                    return redirect('destination_detail', pk=pk)
        else:
            return redirect('login')
    else:
        form = BookingForm(max_people=tour.max_people)
        formcmt = CommentForm()

    context = {
        'tours' : Tour.get_tour_list(3),
        'tour' : tour,
        'form':form,
        'formcmt' : formcmt,
    }
    return render(request, 'destination_detail.html', context)

def contact(request):
    return render(request, 'contact.html')

@login_required
def profile(request):
    if request.user.is_authenticated:
        p = get_object_or_404(User.objects.prefetch_related('booking'), pk=request.user.pk)
    else:
        messages.warning(request,'Không thể tìm thấy trang này')
        return redirect('index')
    context = {
        'p' : p,
    }
    return render(request, 'profile.html', context)

@login_required
def editprofile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.pk)
        if request.method == 'POST':
            form = Editprofile(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.info(request,'Thay đổi thành công!!')
                return redirect('index')
        else:
            form = Editprofile(birthday=user.profile.birthdate, first_name=user.first_name,
                last_name=user.last_name, email=user.email, phone=user.profile.phone_number,
                gender=user.profile.gender, country=user.profile.country)
    else:
        messages.warning(request,'Không thể tìm thấy trang này')
        return redirect('index')
    context = {
        'user' : user,
        'form' : form,
    }
    return render(request, 'edit_profile.html', context)

class SearchResultsView(ListView):
    model = Tour
    template_name = 'search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Tour.objects.filter(
            Q(tour_name__icontains=query) | Q(destination__location_to__icontains=query)
        )
        return object_list

def blog(request):
    blogs = Blog.objects.select_related('user')
    recent_post = Blog.objects.all().order_by('-date')[:6]
    tag = Blog.objects.values('tag').annotate(num_tag=Count('id'))
    if request.method == 'POST':
        if request.user.is_authenticated:
            form=BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.content = form.cleaned_data.get('content')
                blog.title = form.cleaned_data.get('title')
                blog.tag = form.cleaned_data.get('tag')
                blog.user = request.user
                blog.image = form.cleaned_data.get('image')
                blog.save()
                messages.info(request,'Đăng thành công')
                return redirect('blog')
            else:
                return redirect('index')
        else:
            return redirect('login')
    else:
        form=BlogForm()

    context = {
        'form' : form,
        'tag' : tag,
        'blogs' : blogs,
        'recent_post' : recent_post
    }
    return render(request, 'blog.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog.objects.select_related('user'), pk=pk)
    recent_post = Blog.objects.all().order_by('-date')[:6]
    tag = Blog.objects.values('tag').annotate(num_tag=Count('id'))
    context = {
        'tag' : tag,
        'blog' : blog,
        'recent_post' : recent_post
    }
    return render(request, 'blog_detail.html', context)

def destination_area(request, pk):
    arealist = get_object_or_404(Area.objects.prefetch_related('areas', 'areas__tours', 'areas__tours__tour_photo' ,'areas__tours__review'), pk=pk)
    context = {
        'arealist' : arealist,
    }
    return render(request, 'destination_area.html', context)

@login_required
def order(request):
    tour_id = request.session.get('tour_id')
    total_price = request.session.get('total_price')
    people_number = request.session.get('people_number')
    tour = Tour.objects.get(pk=tour_id)
    booking_time = datetime.datetime.now()
    booking = {
        'booking_time' : booking_time,
        'tour' : tour,
        'total_price' : total_price,
        'people_number' : people_number,
    }
    context = {
        'booking' : booking,
    }
    return render(request, 'order.html', context)

@csrf_exempt
def payment_done(request):
    tour_id = request.session.get('tour_id')
    total_price = request.session.get('total_price')
    people_number = request.session.get('people_number')
    tour = Tour.objects.get(pk=tour_id)
    booking = Booking.objects.create(profile=request.user,tour=tour, people_number=people_number, total_price=total_price,)
    booking.status_booking = 1
    booking.save()
    context = {
        'booking' : booking,
        'tour' : tour,
    }
    return render(request, 'done.html', context)

@csrf_exempt
def payment_canceled(request):
    messages.warning(request, 'Thanh toán không thành công')
    return redirect('index')

def payment_process(request):
    tour_id = request.session.get('tour_id')
    total_price = request.session.get('total_price')
    tour = Tour.objects.get(pk=tour_id)
    price = total_price/23178
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % price,
        'amount': '200',
        'item_name': ' {}'.format(tour.tour_name),
        'invoice': '',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'form': form,
    }
    return render(request, 'payment_process.html', context)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    tour_id = request.session.get('tour_id')
    total_price = request.session.get('total_price')
    tour = Tour.objects.get(pk=tour_id)
    price = total_price/23178
    host = request.get_host()
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment/done?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://{}{}'.format(host, reverse('cancelled')),
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': tour.tour_name,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': int(price)*100,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
