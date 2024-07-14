from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars, name='cars'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:car_id>/', views.checkout, name='checkout'),
    
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    path('success/', views.success, name='success'),
    path('search/', views.search_cabs, name='search_cabs'),
    
    path('sendmail_booking/', views.sendmail_booking, name='sendmail_booking'),
    path('sendmail_contact/', views.sendmail_contact, name='sendmail_contact'),
    
    
    
    
    

]