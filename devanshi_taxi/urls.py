from django.urls import path
from . import views
from .views import robots_txt
from .views import BingSiteAuth_xml


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars, name='cars'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:car_id>/', views.checkout, name='checkout'),

    
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    
    path('search/', views.search_cabs, name='search_cabs'),
    path('booking/', views.booking_view, name='booking'),
    path('success/<int:pk>/',views.success, name='success'),

    
    path('sendmail_contact/', views.sendmail_contact, name='sendmail_contact'),
    path('get_fare_summary/<int:car_id>/', views.get_fare_summary, name='get_fare_summary'),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("BingSiteAuth.xml", views.BingSiteAuth_xml, name="BingSiteAuth.xml"),
    
    
    
    
    
    
    
    

]