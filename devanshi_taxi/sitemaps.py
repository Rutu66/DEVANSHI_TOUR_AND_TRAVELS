from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Car, Booking

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['index', 'about', 'contact', 'service']  # Add your static views here

    def location(self, item):
        return reverse(item)

class CarSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Car.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Assuming your model has an `updated_at` DateTimeField

class BookingSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Booking.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Assuming your model has an `updated_at` DateTimeField
