from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate

from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Logger
logger = logging.getLogger(__name__)


# Get Cars
@csrf_exempt
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})

# Login
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            response_data = {
                "userName": username,
                "status": "Authenticated"
            }
        else:
            response_data = {
                "userName": username,
                "status": "Failed"
            }

        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)

# Logout
@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Registration
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    email_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is a new user".format(username))
    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

# Get Dealerships
@csrf_exempt
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Get Dealer Reviews
@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']

        return JsonResponse({"status": 200, "reviews": reviews})

    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Get Dealer Details
@csrf_exempt
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Add Review
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)

        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
