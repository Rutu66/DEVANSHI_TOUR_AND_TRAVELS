from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=100)
    cars = models.ManyToManyField(Car, through='PackageCarRelationship')
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return self.name

class PackageCarRelationship(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.package.name} - {self.car.name}"
