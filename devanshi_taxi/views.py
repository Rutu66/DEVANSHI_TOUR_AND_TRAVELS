from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from .models import *  # Adjust imports as per your app structure
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect




def search_cabs(request):
    """
    View function for searching available cars based on user input.
    Handles GET and POST requests to display available cars or handle form submissions.
    """
    if request.method == 'POST':
        # Retrieve form data
        travel_type = request.POST.get('travel_type')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        return_date = request.POST.get('return_date')

        # Ensure required fields are filled
        if not (travel_type and pickup and drop and pickup_date and pickup_time):
            return render(request, 'cars.html', {'error_message': 'Please fill all required fields.'})

        # Convert date strings to datetime objects for comparison
        pickup_datetime = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_datetime = datetime.strptime(return_date, '%Y-%m-%d') if return_date else None

        # Check if return date is before pickup date for round trip
        if travel_type == 'round_trip' and return_datetime and return_datetime < pickup_datetime:
            return render(request, 'cars.html', {'error_message': 'Return date cannot be before pickup date.'})

        # Retrieve all cars from the Car model
        cars = Car.objects.all()

        # Context to be passed to the template
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

    # For GET requests, just render the search form
    return render(request, 'cars.html')


def booking_view(request):
    """
    View function for handling booking form submission.
    Creates a new Booking object and sends confirmation emails.
    """
    if request.method == 'POST':
        try:
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
            return_date_str = request.POST.get('return_date')

            # Convert return date string to datetime object if provided
            if return_date_str:
                try:
                    return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponse('Invalid return date format. Must be YYYY-MM-DD.')
            else:
                return_date = None

            route = request.POST.get('route')

            # Create Booking object in the database
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
            )

            # Send confirmation emails to customer and owner
            email_content_customer = render_to_string('booking_confirmation_email.html', {
                'username': username,
                'email': email,
                'mobile': mobile,
                'alt_mobile': alt_mobile,
                'pickup': pickup,
                'drop': drop,
                'num_passengers': num_passengers,
                'travel_type': travel_type,
                'pickup_date': pickup_date,
                'pickup_time': pickup_time,
                'return_date': return_date,
                'route': route,
            })
            send_mail('Booking Confirmation', '', settings.DEFAULT_FROM_EMAIL, [email], html_message=email_content_customer)

            email_content_owner = render_to_string('new_booking_email.html', {
                'username': username,
                'email': email,
                'mobile': mobile,
                'alt_mobile': alt_mobile,
                'pickup': pickup,
                'drop': drop,
                'num_passengers': num_passengers,
                'travel_type': travel_type,
                'pickup_date': pickup_date,
                'pickup_time': pickup_time,
                'return_date': return_date,
                'route': route,
            })
            send_mail('New Booking Received', '', settings.DEFAULT_FROM_EMAIL, ['booking@devanshitours.com'], html_message=email_content_owner)

            # Return JSON response with redirect URL
            return JsonResponse({'redirect_url': f'/success/{booking.pk}/'})

        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponse('An error occurred during the booking process.')

    return render(request, 'booking.html')


def sendmail_contact(request):
    """
    View function for sending contact details via email.
    """
    if request.method == "POST":
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile', '')
        message = request.POST.get('message', '')

        context = {
            'name': name,
            'mobile': mobile,
            'message': message,
        }

        html_message = render_to_string('email_template.html', context)

        send_mail(
            "Received contact details",
            '',
            'devanshicab99@gmail.com',
            ['booking@devanshitours.com'],
            fail_silently=False,
            html_message=html_message,
        )

        messages.success(request, "Your information was sent successfully")

    return redirect('contact')


def index(request):
    """
    View function for rendering the index page with a list of cars.
    """
    car_list = Car.objects.all()

    data = {
        'car_list': car_list
    }

    return render(request, 'index.html', data)


def cars(request):
    """
    View function for rendering the cars page with car search parameters.
    """
    car_list = Car.objects.all()

    travel_type = request.GET.get('travel_type', '')
    pickup_location = request.GET.get('pickup', '')
    drop_location = request.GET.get('drop', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    return_date = request.GET.get('return_date', '')

    return render(request, 'cars.html', {
        'travel_type': travel_type,
        'pickup_location': pickup_location,
        'drop_location': drop_location,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'return_date': return_date,
        'car_list': car_list,
    })


def checkout(request, car_id):
    """
    View function for handling checkout process for car booking.
    """
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        pickup_date = request.POST.get('pickup_date', '')
        pickup_time = request.POST.get('pickup_time', '')
        travel_type = request.POST.get('trip_type', '')
        return_date = request.POST.get('return_date', '')
        pickup_location = request.POST.get('pickup_location', '')
        drop_location = request.POST.get('drop_location', '')

        context = {
            'car': car,
            'pickup_date': pickup_date,
            'pickup_time': pickup_time,
            'travel_type': travel_type,
            'return_date': return_date,
            'pickup_location': pickup_location,
            'drop_location': drop_location,
        }
        return render(request, 'checkout.html', context)

    return render(request, 'error.html', {'message': 'Invalid request method'})


def about(request):
    """
    View function for rendering the about page.
    """
    return render(request, 'about.html')


def contact(request):
    """
    View function for rendering the contact page.
    """
    return render(request, 'contact.html')


def service(request):
    """
    View function for rendering the service page.
    """
    return render(request, 'service.html')


def success(request, pk):
    """
    View function for rendering the success page with booking details.
    """
    booking = Booking.objects.get(pk=pk)
    return render(request, 'success.html', {'booking': booking})


def get_fare_summary(request, car_id):
    """
    View function for retrieving fare summary for a specific car.
    Returns JSON response with fare details.
    """
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
