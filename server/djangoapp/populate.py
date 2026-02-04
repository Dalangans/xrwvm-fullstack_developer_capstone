from .models import CarMake, CarModel, Dealership, Review
from django.contrib.auth.models import User
import json
import os

def initiate():
    # Create CarMake instances
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(
                name=data['name'],
                description=data['description']
            )
        )
    
    # Create CarModel instances
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "make": car_make_instances[0], "dealer_id": 1},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "make": car_make_instances[0], "dealer_id": 2},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "make": car_make_instances[0], "dealer_id": 3},
        {"name": "A-Class", "type": "SUV", "year": 2023, "make": car_make_instances[1], "dealer_id": 4},
        {"name": "C-Class", "type": "SUV", "year": 2023, "make": car_make_instances[1], "dealer_id": 5},
        {"name": "E-Class", "type": "SUV", "year": 2023, "make": car_make_instances[1], "dealer_id": 6},
        {"name": "A4", "type": "SUV", "year": 2023, "make": car_make_instances[2], "dealer_id": 7},
        {"name": "A5", "type": "SUV", "year": 2023, "make": car_make_instances[2], "dealer_id": 8},
        {"name": "A6", "type": "SUV", "year": 2023, "make": car_make_instances[2], "dealer_id": 9},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "make": car_make_instances[3], "dealer_id": 10},
        {"name": "Carnival", "type": "SUV", "year": 2023, "make": car_make_instances[3], "dealer_id": 11},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "make": car_make_instances[3], "dealer_id": 12},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "make": car_make_instances[4], "dealer_id": 13},
        {"name": "Camry", "type": "Sedan", "year": 2023, "make": car_make_instances[4], "dealer_id": 14},
        {"name": "Kluger", "type": "SUV", "year": 2023, "make": car_make_instances[4], "dealer_id": 15},
    ]
    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            make=data['make'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id']
        )

    # Create dealerships from JSON file
    dealerships_json_path = os.path.join(os.path.dirname(__file__), '../database/data/dealerships.json')
    if os.path.exists(dealerships_json_path):
        try:
            with open(dealerships_json_path, 'r') as f:
                dealerships_data = json.load(f)
                for dealer_data in dealerships_data.get('dealerships', []):
                    Dealership.objects.get_or_create(
                        id=dealer_data.get('id'),
                        defaults={
                            'name': dealer_data.get('full_name', dealer_data.get('short_name', '')),
                            'city': dealer_data.get('city', ''),
                            'address': dealer_data.get('address', ''),
                            'zip': dealer_data.get('zip', ''),
                            'lat': dealer_data.get('lat', 0),
                            'long': dealer_data.get('long', 0),
                            'state': dealer_data.get('state', ''),
                        }
                    )
                print(f"Dealerships created successfully")
        except Exception as e:
            print(f"Error loading dealerships: {e}")
    else:
        print(f"Dealerships JSON file not found at {dealerships_json_path}")
    
    # Create test users
    test_users = [
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@dealership.com', 'first_name': 'Admin', 'last_name': 'User'},
        {'username': 'testuser', 'password': 'test123', 'email': 'test@dealership.com', 'first_name': 'Test', 'last_name': 'User'},
        {'username': 'john', 'password': 'john123', 'email': 'john@dealership.com', 'first_name': 'John', 'last_name': 'Doe'},
    ]

    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f"User {user_data['username']} created successfully")
