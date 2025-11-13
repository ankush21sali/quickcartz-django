from django.shortcuts import render, redirect
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart, CartItem

import requests

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account!"
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # redirect page for email verification
            return redirect(f'/accounts/login/?command=verification&email={email}')
        
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

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)

                for item in cart_items:
                    # check if same product + variant already exists for this user
                    existing_item = CartItem.objects.filter(
                        user=user,
                        product=item.product,
                        variant=item.variant
                    ).first()

                    if existing_item:
                        # if found → just increase quantity
                        existing_item.quantity += item.quantity
                        existing_item.save()
                        item.delete()
                    else:
                        # otherwise → assign the user to guest item
                        item.user = user
                        item.cart = None
                        item.save()

            except Cart.DoesNotExist:
                pass

            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")

            # Redirect dynamically to 'next' if it exists
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))

                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')



def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')



@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = "Please activate your account!"
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    
    return render(request, 'accounts/forgotPassword.html')



def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            # Set New Password of user
            user.set_password(password)
            user.save()
    
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')