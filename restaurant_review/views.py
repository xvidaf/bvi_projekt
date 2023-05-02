import time

from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


from web_honeypot.models import HoneypotSetting, RestaurantLog, ReviewLog, SqlLog
from web_honeypot.utils import log_previous_page, log_sql
from restaurant_review.models import Restaurant, Review

# Create your views here.

def index(request):
    print('Request for index page received')

    log_previous_page(request)

    restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review'))
    print(restaurants)
    log_sql(request, "ALL_RESTAURANTS")
    return render(request, 'restaurant_review/index.html', {'restaurants': restaurants})


def details(request, id):
    print('Request for restaurant details page received')

    log_previous_page(request)

    restaurant = get_object_or_404(Restaurant, pk=id)
    log_sql(request, "DETAIL_RESTAURANT")
    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})


def create_restaurant(request):
    print('Request for add restaurant page received')

    log_previous_page(request)

    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
    except (KeyError):
        # Redisplay the form
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description

        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip_address = user_ip.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if HoneypotSetting.objects.first().log_restaurant_creation is True:
            RestaurantLog.objects.create(
                name=name,
                street_address=street_address,
                description=description,
                session_key=request.session.session_key,
                ip_address=ip_address.split(':')[0],
                user_agent=request.META.get('HTTP_USER_AGENT'),
            )
        if HoneypotSetting.objects.first().allow_review_creation is True:
            Restaurant.save(restaurant)
            log_sql(request, "CREATE_RESTAURANT")
        else:
            restaurant.id = 1

        return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))


@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        # Redisplay the form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip_address = user_ip.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        if HoneypotSetting.objects.first().log_review_creation is True:
            ReviewLog.objects.create(
                restaurant=restaurant.id,
                name=user_name,
                rating=rating,
                comment=review_text,
                session_key=request.session.session_key,
                ip_address=ip_address.split(':')[0],
                user_agent=request.META.get('HTTP_USER_AGENT'),
            )

        if HoneypotSetting.objects.first().allow_review_creation is True:
            Review.save(review)
            log_sql(request, "CREATE_REVIEW")

    return HttpResponseRedirect(reverse('details', args=(id,)))
