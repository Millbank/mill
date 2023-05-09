from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.middleware import csrf
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid or has expired')
        return redirect('home')

def new_user(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        password = escape(request.POST['password'])
        password2 = escape(request.POST['password2'])
        email = escape(request.POST['email'])


        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'new_user.html', {'csrf_token': csrf.get_token(request)})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'new_user.html', {'csrf_token': csrf.get_token(request)})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'new_user.html', {'csrf_token': csrf.get_token(request)})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = f"{request.scheme}://{request.get_host()}/activate/{uidb64}/{token}"

        # Send activation email to the user
        send_mail(
            'Activate your account',
            f'Please click the following link to activate your account: {activation_url}',
            'noreply@yourdomain.com',  # Replace with your email address
            [email],
            fail_silently=False,
        )

        messages.success(request, 'Registration successful. Please check your email to activate your account.')
        return redirect('home')
    else:
        return render(request, 'new_user.html', {'csrf_token': csrf.get_token(request)})


def new_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_type = request.POST.get('product_type')
        cost_price = request.POST.get('cost_price')
        quantity = request.POST.get('quantity')
        manufacturer = request.POST.get('manufacturer')
        batch_number = request.POST.get('batch_number')
        description = request.POST.get('description')

        # Create a new product instance with the form data
        if product_name.ojects.filter(product_name=product_name).exists:
            messages.error(request, 'Product already exist in system')
            new_product = Product(
                product_name=product_name,
                product_type=product_type,
                price=price,
                quantity=quantity,
                manufacturer=manufacturer,
                batch_number=batch_number,
                description=description,
            )

        # Save the new product instance to the database
        new_product.save()

        # Redirect to the dashboard page after successful form submission
        return HttpResponseRedirect('/dashboard/')

    # Render the product creation form template if the request is not a POST request
    return render(request, 'product_create.html')


def home(request):
    return render(request, 'home.html')

def stock_update(request):
    return render(request, 'stock_update')

def dashboard(request):
    return render(request, 'dashboard.html')
