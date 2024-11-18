from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .tasks import process_csv


def home_page(request):
    return render(request , 'home.html')


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        csv_data = csv_file.read()

        user_email = request.user.email 
        process_csv.delay(csv_data, user_email)
    
        messages.success(request, "CSV file upload initiated. You'll receive an email when processing is complete.")
        return redirect('home')  

    return render(request, 'upload.html')



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request,'login.html')


@login_required
def logout_page(request):
    logout(request)  
    messages.success(request, 'You have been logged out successfully.') 
    return redirect('home') 


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password1 != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please try another.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, 
                                        email=email,
                                        password=password1
                                        )
        user.save()
        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request, 'signup.html')

