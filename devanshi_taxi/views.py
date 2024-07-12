from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from devanshi_taxi.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
# from django.contrib.auth import logout, authenticate, login as l 
from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from django.conf import settings




# Create your views here.
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

def sendmail_booking(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        cartype = request.POST.get('cars', '')
        pickup = request.POST.get('pickup', '')
        drop = request.POST.get('drop', '')
        mobail = request.POST.get('mobail', '')

        full_message = f"""
            Name: {name}
            Car Type: {cartype}
            From: {pickup}
            To: {drop}
            Mobile No: {mobail}
        """

        send_mail(
            "Received booking details from yashtaxi",
            full_message,
            'yashtaxi2000@gmail.com',
            ['rutukotadiya999@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Your information was sent successfully.")
        return redirect('index')

    # Handle GET request or other scenarios where POST data is not available
    return redirect('index')  # Redirect to index or another appropriate view


def sendmail_contact(request):
    
    if request.method == "POST":
       
       
        
        name = request.POST.get('name', '')
        
        mobile = request.POST.get('mobile', '')  # Use the correct key here
        message = request.POST.get('message', '')
        
    full_message = f"""
        Received message below from {name}
        
        .....................................
        
        massage : {message}
        mobail no : {mobile}
    """ 
    send_mail(
        "Receve contact details from yashtaxi",
        full_message,
        'yashtaxi2000@gmail.com',
        ['rutukotadiya999@gmail.com'],
        fail_silently=False,
          
    )
    messages.success(request, " your information send succsessfully ")
    
    return redirect('contact')
    



def index(request):
    
    
    car_list = Cars.objects.all()
    
    data = {
        'car_list': car_list
       
        
    }
    
    return render(request, 'index.html', data)


def cars(request):
    """ For cars page...."""
    car_list = Cars.objects.all()


    # Pass the data to the template
    # trip_type = request.GET.get('trip_type', '')
    travel_type = request.GET.get('travel_type', '')
    pickup_location = request.GET.get('pickup', '')
    drop_location = request.GET.get('drop', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    return_date = request.GET.get('return_date', '')

    # Pass the data to the template
    return render(request, 'cars.html', {
        # 'trip_type': trip_type,
        'travel_type' : travel_type,
        'pickup_location': pickup_location,
        'drop_location': drop_location,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'return_date': return_date,
        'car_list': car_list,
    })
    
        

    
    
    
    

def checkout(request, car_id):
    """ For about page...."""
    car = get_object_or_404(Cars, id=car_id)
    # Pass the data to the template
    return render(request, 'checkout.html', {'car': car})


def about(request):
    """ For about page...."""
    
    
    
    return render(request, 'about.html')

def contact(request):
    """ For contact page...."""
    
    
    return render(request, 'contact.html')

def service(request):
    """ For service page..."""
    
   
    
    return render(request, 'service.html')



# **************************************************************************

# views.py

from django.shortcuts import render
from .models import Cars, Price
from datetime import datetime

def search_cabs_view(request):
    if request.method == 'GET':
        travel_type = request.GET.get('travel_type')
        pickup = request.GET.get('pickup')
        drop = request.GET.get('drop')
        pickup_date = request.GET.get('pickup_date')
        pickup_time = request.GET.get('pickup_time')
        return_date = request.GET.get('return_date')
        
        # Parse pickup date and time into a datetime object
        pickup_datetime = datetime.strptime(pickup_date + ' ' + pickup_time, '%Y-%m-%d %H:%M')
        
        # Adjust return date format if available
        formatted_return_date = datetime.strptime(return_date, '%Y-%m-%d').strftime('%d/%m/%y') if return_date else None
        
        # Query based on trip type and travel type
        cars = Cars.objects.filter(prices__pickup_location=pickup, prices__drop_location=drop)
        
        if travel_type == 'one_way':
            cars = cars.filter(prices__pickup_location=pickup, prices__drop_location=drop)
        elif travel_type == 'round_trip':
            cars = cars.filter(prices__pickup_location=pickup, prices__drop_location=drop)
        
        context = {
            'cars': cars.distinct(),  # Ensure each car appears only once
            'pickup': pickup,
            'drop': drop,
            'pickup_datetime': pickup_datetime,
            'return_date': formatted_return_date,
            'travel_type': travel_type,
        }
        
        return render(request, 'cars.html', context)
