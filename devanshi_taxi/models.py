from django.db import models



class Cars(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars/images/', blank=True)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Price(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='prices')
    pickup_location = models.CharField(max_length=100)
    drop_location = models.CharField(max_length=100)
    price_per_km = models.DecimalField(max_digits=8, decimal_places=2)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car.name} - {self.pickup_location} to {self.drop_location}"
    
