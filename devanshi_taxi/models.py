# models.py
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='car_images/')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class Route(models.Model):
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.pickup} to {self.drop} ({self.distance} km)"
    
    
class Cost(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    extra_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cost for {self.car} on {self.route}"
    


