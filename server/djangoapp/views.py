from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_page(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/static.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
def get_index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    elif request.method == "POST":
        # Process the login request here
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')  # Redirect to the desired page after successful login
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/fdeb696a-7e2d-4899-9155-a4a235f9b6ba/dealership-package/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        print(dealerships)
        # for dealer in dealerships:
        #     print(dealer.id)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

def get_dealership_by_id(request, dealer_id):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/fdeb696a-7e2d-4899-9155-a4a235f9b6ba/dealership-package/dealership"
        # Get dealers from the URL
        dealerships = get_dealer_by_id(url, dealer_id)
        # Concat all dealer's short name
        dealer_names = ' - '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"https://eu-gb.functions.appdomain.cloud/api/v1/web/fdeb696a-7e2d-4899-9155-a4a235f9b6ba/dealership-package/get-review?id={dealer_id}"
        # Get reviews from the URL
        reviews = get_dealer_by_id_from_cf(url, id=dealer_id)
        # Concat all review's comment
        review_service = ' - '.join([rev.review + " -> sentiment: " + rev.sentiment for rev in reviews])
        # Return a list of review's comment
        return HttpResponse(review_service)


def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return redirect("/djangoapp/login")

    context = {}
    dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/fdeb696a-7e2d-4899-9155-a4a235f9b6ba/dealership-package/dealership"
    dealers = get_dealers_from_cf(dealer_url)
    context["dealers"] = dealers
    context["dealer_id"] = dealer_id

    if request.method == "GET":
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        form = request.POST
        review = {
            "dealership": dealer_id,
            "name": f"{request.user.first_name} {request.user.last_name}",
            "review": form.get("content"),
            "purchase": form.get("purchasecheck") == "on",
            "purchase_date": form.get("purchasedate", None),
            "car_make": None,
            "car_model": None,
            "car_year": None,
        }

        if review["purchase"]:
            car_id = form.get("car")
            if car_id:
                try:
                    car = CarModel.objects.get(pk=car_id)
                    review["car_make"] = car.make.name
                    review["car_model"] = car.name
                    review["car_year"] = car.year.strftime("%Y")
                except CarModel.DoesNotExist:
                    pass

        post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/fdeb696a-7e2d-4899-9155-a4a235f9b6ba/dealership-package/post-review"
        json_payload = {"review": review}
        post_request(post_url, json_payload, dealer_id=dealer_id)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
