from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from devanshi_taxi.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


from django.shortcuts import render
from .models import Cost  # Import relevant models

def search_cabs(request):
    if request.method == 'GET':
        travel_type = request.GET.get('travel_type')
        pickup = request.GET.get('pickup')
        drop = request.GET.get('drop')
        pickup_date = request.GET.get('pickup_date')
        pickup_time = request.GET.get('pickup_time')
        return_date = request.GET.get('return_date')

        # Ensure required fields are filled
        if not (travel_type and pickup and drop and pickup_date and pickup_time):
            return render(request, 'your_template.html', {'error_message': 'Please fill all required fields.'})

        # Filter cars based on pickup and drop locations and travel type
        cars = Cost.objects.filter(
            route__pickup__icontains=pickup,
            route__drop__icontains=drop,
        )

        context = {
            'cars': cars,
            'travel_type': travel_type,
            'pickup': pickup,
            'drop': drop,
            'pickup_date': pickup_date,
            'pickup_time': pickup_time,
            'return_date': return_date,
        }

        return render(request, 'cars.html', context)
    
    return render(request,'search.html')
    


def booking_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        alt_mobile = request.POST.get('alt_mobile')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        num_passengers = request.POST.get('num_passengers')
        travel_type = request.POST.get('travel_type')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        return_date_str = request.POST.get('return_date')  # Get return_date as string

        # Convert return_date_str to datetime object if not empty
        if return_date_str:
            try:
                return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse('Invalid return date format. Must be YYYY-MM-DD.')
        else:
            return_date = None  # Handle case where return_date is not provided

        route = request.POST.get('route')
        full_payable_amount = request.POST.get('full_payable_amount')

        # Create Booking object
        booking = Booking.objects.create(
            username=username,
            email=email,
            mobile=mobile,
            alt_mobile=alt_mobile,
            pickup=pickup,
            drop=drop,
            num_passengers=num_passengers,
            travel_type=travel_type,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            return_date=return_date,
            route=route,
            full_payable_amount=full_payable_amount
        )

        # Send email with booking details to recipient (customer)
        subject_customer = 'Booking Confirmation'
        message_customer = f'Hello {username},\n\nYour booking details:\n\nPickup: {pickup}\nDrop: {drop}\nPickup Date: {pickup_date}\n\nThank you!'
        recipient_customer = [email]  # Use the email entered by the user as recipient for customer

        send_mail(subject_customer, message_customer, settings.DEFAULT_FROM_EMAIL, recipient_customer)

        # Send email with booking details to owner (replace 'owner_email' with actual owner's email)
        subject_owner = 'New Booking Received'
        message_owner = f'Hello,\n\nA new booking has been received:\n\nUsername: {username}\nEmail: {email}\nMobile: {mobile}\nPickup: {pickup}\nDrop: {drop}\nPickup Date: {pickup_date}\n\nPlease take necessary actions.'
        recipient_owner = ['devanshicab99@gmail.com']  # Replace with actual owner's email address

        send_mail(subject_owner, message_owner, settings.DEFAULT_FROM_EMAIL, recipient_owner)

        # Redirect to a success URL with pk
        return redirect('success', pk=booking.pk)  # Replace 'success' with your actual success URL name

    return render(request, 'booking.html')



def sendmail_contact(request):
    
    if request.method == "POST":
       
        name = request.POST.get('name', '')
        
        mobile = request.POST.get('mobile', '')  # Use the correct key here
        message = request   .POST.get('message', '')
        
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
    
    
    car_list = Car.objects.all()
    
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
    


from django.shortcuts import render, get_object_or_404
from .models import Cost

def checkout(request, car_id):
    cost_instance = get_object_or_404(Cost, id=car_id)
    car = cost_instance.car
    route = cost_instance.route
    total_fare = cost_instance.total_fare
    extra_fare = cost_instance.extra_fare

    # Fetch additional data from the request.GET
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    travel_type = request.GET.get('trip_type', '')  # Assuming 'trip_type' is passed from the template

    return_date = None
    if travel_type == 'round_trip':
        return_date = request.GET.get('return_date', '')

    # Print route information for debugging purposes
    print(route)

    return render(request, 'checkout.html', {
        'car': car,
        'route': route,
        'total_fare': total_fare,
        'extra_fare': extra_fare,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'travel_type': travel_type,
        'return_date': return_date,
    })




def about(request):
    """ For about page...."""
    
    
    
    return render(request, 'about.html')

def contact(request):
    """ For contact page...."""
    
    
    return render(request, 'contact.html')

def service(request):
    """ For service page..."""
    
   
    
    return render(request, 'service.html')


def success(request, pk):
    """ For success page..."""
    
    booking = Booking.objects.get(pk=pk)
    return render(request, 'success.html', {'booking': booking})


from django.http import JsonResponse


def get_fare_summary(request, car_id):
    cost = get_object_or_404(Cost, id=car_id)
    distance = cost.route.distance
    gst = cost.total_fare * 5 / 100
    estimated_amount = cost.total_fare - gst
    
    data = {
        'estimated_amount': estimated_amount,
        'covered_kms': distance,
        'gst': gst,
        'total_cost': cost.total_fare
    }

    return JsonResponse(data)
