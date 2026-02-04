# Uncomment the required imports before adding the code

from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel, Dealership, Review
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    else:
        response_data = {"userName": username, "status": "Incorrect username or password"}
    return JsonResponse(response_data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False  # Gunakan nama ini
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:  # noqa: E722
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName":username, "status":"Authenticated"})
    else:
        return JsonResponse({"userName":username, "error":"Already Registered"})
        
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="All"):
    # Fetch dealerships from Django database instead of Node.js backend
    try:
        if state == "All":
            dealerships = Dealership.objects.all()
        else:
            dealerships = Dealership.objects.filter(state=state)
        
        dealers_list = []
        for dealer in dealerships:
            dealers_list.append({
                "id": dealer.id,
                "name": dealer.name,
                "city": dealer.city,
                "address": dealer.address,
                "zip": dealer.zip,
                "lat": dealer.lat,
                "long": dealer.long,
                "state": dealer.state,
                "short_name": dealer.name.split()[0] if dealer.name else ""
            })
        return JsonResponse({"status": 200, "dealers": dealers_list})
    except Exception as e:
        logger.error(f"Error fetching dealerships: {e}")
        return JsonResponse({"status": 500, "dealers": [], "error": str(e)})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    try:
        dealership = Dealership.objects.get(id=dealer_id)
        dealer_dict = {
            "id": dealership.id,
            "name": dealership.name,
            "city": dealership.city,
            "address": dealership.address,
            "zip": dealership.zip,
            "lat": dealership.lat,
            "long": dealership.long,
            "state": dealership.state,
            "short_name": dealership.name.split()[0] if dealership.name else ""
        }
        return JsonResponse({"status": 200, "dealer": dealer_dict})
    except Dealership.DoesNotExist:
        return JsonResponse({"status": 404, "error": "Dealership not found"})
    except Exception as e:
        logger.error(f"Error fetching dealer details: {e}")
        return JsonResponse({"status": 500, "error": str(e)})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = Review.objects.filter(dealership_id=dealer_id)
        reviews_list = []
        for review in reviews:
            review_dict = {
                "id": review.id,
                "dealership": review.dealership.id,
                "name": review.name,
                "purchase": review.purchase,
                "review": review.review,
                "purchase_date": review.purchase_date.isoformat() if review.purchase_date else None,
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
                "sentiment": review.sentiment,
                "created_at": review.created_at.isoformat()
            }
            reviews_list.append(review_dict)
        return JsonResponse({"status": 200, "reviews": reviews_list})
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        return JsonResponse({"status": 500, "reviews": [], "error": str(e)})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous is False:
        data = json.loads(request.body)
        try:
            dealership_id = data.get('dealership')
            dealership = Dealership.objects.get(id=dealership_id)
            
            # Analyze sentiment
            review_text = data.get('review', '')
            sentiment = 'neutral'
            try:
                sentiment_result = analyze_review_sentiments(review_text)
                sentiment = sentiment_result.get('sentiment', 'neutral') if sentiment_result else 'neutral'
            except Exception as e:
                logger.error(f"Error analyzing sentiment: {e}")
            
            # Create review
            review = Review.objects.create(
                dealership=dealership,
                name=data.get('name', request.user.username),
                purchase=data.get('purchase', False),
                review=review_text,
                purchase_date=data.get('purchase_date', None),
                car_make=data.get('car_make', ''),
                car_model=data.get('car_model', ''),
                car_year=data.get('car_year', None),
                sentiment=sentiment
            )
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Dealership.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Dealership not found"})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": f"Error in posting review: {str(e)}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.make.name})
    return JsonResponse({"CarModels":cars})
# ...