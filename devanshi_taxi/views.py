from django.shortcuts import render
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
        name = request.POST['name']
        mobail = request.POST['mobail']
        message = request.POST['message']
        
    full_message = f"""
        Received message below from {name}
        
        .....................................
        
        massage : {message}
        mobail no : {mobail}
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
    
    
    car_list = Car.objects.all()
    packages = Package.objects.all()
    
    
    package_list = []   
    for package in packages:
        package_car_relationships = PackageCarRelationship.objects.filter(package=package)
        package_cars = []
        for relationship in package_car_relationships:
            package_cars.append({
                'car': relationship.car,
                'price': relationship.price,
            })
        package_list.append({
            'package': package,
            'cars': package_cars,
        })
    
    data = {
        'car_list': car_list,
        'package_list': package_list,
        
    }
    
    return render(request, 'index.html', data)



def about(request):
    """ For about page...."""
    
    
    
    return render(request, 'about.html')

def contact(request):
    """ For contact page...."""
    
    
    return render(request, 'contact.html')

def service(request):
    """ For service page..."""
    
    packages = Package.objects.all()
    
    package_list = []
    for package in packages:
        package_car_relationships = PackageCarRelationship.objects.filter(package=package)
        package_cars = []
        for relationship in package_car_relationships:
            package_cars.append({
                'car': relationship.car,
                'price': relationship.price,
            })
        package_list.append({
            'package': package,
            'cars': package_cars,
        })
    
    data = {
        'package_list': package_list
    }
    
    return render(request, 'service.html', data)