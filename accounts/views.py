from django.shortcuts import render, redirect
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
    
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #create username is automatically unique-like (based on their email).
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email, username=username, 
                password=password
                )
            
            user.phone_number = phone_number
            user.save()
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # redirect to your login page
        
        else:
            # form is invalid (maybe missing field, etc.)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)



def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')



def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')



def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if email exists
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, 'No account found with that email!')
            return redirect('forgot_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('forgot_password')

        # Update password
        user.set_password(password)
        user.save()

        messages.success(request, 'Password reset successful! You can now log in.')
        return redirect('login')
    
    return render(request, 'accounts/forgot_password.html')