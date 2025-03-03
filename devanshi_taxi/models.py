# models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone



class Car(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
        ('Minivan', 'Minivan'),
        ('Pickup Truck', 'Pickup Truck'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='car_images/')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    capacity = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)  # Add this field


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('car_detail', args=[str(self.id)])

# class Route(models.Model):
#     pickup = models.CharField(max_length=255)
#     drop = models.CharField(max_length=255)
#     distance = models.DecimalField(max_digits=6, decimal_places=2)

#     def __str__(self):
#         return f"{self.pickup} to {self.drop} ({self.distance} km)"
    
    
# class Cost(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     route = models.ForeignKey(Route, on_delete=models.CASCADE)
#     total_fare = models.DecimalField(max_digits=10, decimal_places=2)
#     extra_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f"Cost for {self.car} on {self.route}"
    
class Booking(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    alt_mobile = models.CharField(max_length=10, blank=True, null=True)
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    num_passengers = models.IntegerField()
    travel_type = models.CharField(max_length=20)  # New field for travel type
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    return_date = models.DateField(blank=True, null=True)  # New field for return date
    route = models.CharField(max_length=255, blank=True, null=True)  # New field for route
    # full_payable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)  # Added this line


    def __str__(self):
        return f"{self.username} - {self.pickup} to {self.drop}"
    
    def get_absolute_url(self):
        return reverse('booking_detail', args=[str(self.id)])



