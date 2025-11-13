from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, ProductVariant
from .models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        selected_size = request.POST.get('size')
        selected_color = request.POST.get('color') 

        if not selected_color or not selected_size:
            messages.error(request, "Please select a color and size! before adding to cart.")
            return redirect(product.get_url())
        
        # Get or create the variant
        variant, created = ProductVariant.objects.get_or_create(
            product=product,
            color=selected_color,
            size=selected_size,
            # defaults={'stock': 0, 'price': product.price}
        )


        if request.user.is_authenticated:
            # For logged-in user
            cart_item, item_created = CartItem.objects.get_or_create(
                product=product,
                variant=variant,
                user=request.user,
                defaults={'quantity': 1}  # Start with 1 if new
            )    
        else:
            # For guest user → use session cart
            cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
            cart_item, item_created = CartItem.objects.get_or_create(
                product=product,
                variant=variant,
                cart=cart,
                defaults={'quantity': 1}  # Start with 1 if new
            )
        
        # If item already exists, increase quantity
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    
    # fallback
    return redirect(product.get_url())



def add_quantity(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.user.is_authenticated:
        # Logged-in user → cart is linked to user
        cart_item = CartItem.objects.get(
            product=product,
            variant=variant,
            user = request.user
        )
    else:
        # Guest user → cart is linked to session
        cart = Cart.objects.get_object_or_404(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, 
            variant=variant, 
            cart=cart
        )
        
    cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart')



def remove_quantity(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.user.is_authenticated:
        # Logged-in user → cart is linked to user
        cart_item = CartItem.objects.get(
            product=product,
            variant=variant,
            user=request.user
        )
    else:
        # Guest user → cart is linked to session
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, 
            variant=variant, 
            cart=cart
        )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



def remove_cart_item(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.user.is_authenticated:
        # Logged-in user → cart is linked to user
        cart_item = CartItem.objects.get(
            product=product,
            variant=variant,
            user=request.user
        )
    else:
        # Guest user → cart is linked to session
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, 
            variant=variant, 
            cart=cart
        )

    cart_item.delete()

    return redirect('cart')



def cart(request, cart_items=None):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    # Example: 2% GST tax (you can change this)
    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'carts/cart.html',context)



@login_required(login_url= 'login')
def checkout(request, cart_items=None):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    # Example: 2% GST tax (you can change this).
    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'carts/checkout.html', context)