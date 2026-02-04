from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.

class CarMake(models.Model):
    """Model to store car make information"""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Model to store car model information"""
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TRUCK = 'Truck'
    COUPE = 'Coupe'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck'),
        (COUPE, 'Coupe'),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES)
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"


class Dealership(models.Model):
    """Model to store dealership information"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    lat = models.FloatField()
    long = models.FloatField()
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model to store dealer reviews"""
    id = models.IntegerField(primary_key=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    review = models.TextField()
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, null=True, blank=True)
    car_model = models.CharField(max_length=100, null=True, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=50, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.dealership.name} by {self.name}"
