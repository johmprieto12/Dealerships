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
#from .restapis import get_dealers_from_cf


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")
    # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            response_data = {
                "userName": username,
                "status": "Authenticated"
            }
        # If user is valid, call login method to login current user
        else:
            response_data = {
                "userName": username,
                "status": "Failed"
            }
        return JsonResponse(response_data)
    return JsonResponse({"error": "Invalid request"}, status=400)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/<your-namespace>/<your-package>/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context = {"dealership_list": dealerships}
        return render(request, "djangoapp/index.html", context)

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/<your-namespace>/<your-package>/api/review"
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context = {"reviews": reviews, "dealer_id": dealer_id}
    return render(request, 'djangoapp/dealer_reviews.html', context)

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/<your-namespace>/<your-package>/api/dealership"
    dealer = get_dealer_by_id_from_cf(url, dealer_id)
    context = {"dealer": dealer}
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request):
    if request.method == "POST":
        review = {
            "name": request.user.username,
            "dealership": request.POST["dealer_id"],
            "review": request.POST["review"],
            "purchase": request.POST.get("purchase", False),
            "purchase_date": request.POST.get("purchase_date", ""),
            "car_make": request.POST.get("car_make", ""),
            "car_model": request.POST.get("car_model", ""),
            "car_year": request.POST.get("car_year", ""),
        }

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/<your-namespace>/<your-package>/api/review"
        json_payload = {"review": review}

        post_request(url, json_payload)

        return redirect("dealer_details", dealer_id=review["dealership"])