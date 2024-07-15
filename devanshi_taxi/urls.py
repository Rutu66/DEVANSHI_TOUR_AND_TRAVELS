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
    
    path('search/', views.search_cabs, name='search_cabs'),
    path('booking/', views.booking_view, name='booking'),
    path('success/<int:pk>/',views.success, name='success'),

    
    path('sendmail_contact/', views.sendmail_contact, name='sendmail_contact'),
    
    
    
    
    

]