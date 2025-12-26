from django.shortcuts import render, get_object_or_404, redirect
from . models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator

from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


# Create your views here.
def store(request, category_slug=None):
    category  = None
    products = None

    if category_slug != None:
        category  = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category , is_available=True)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    product_count = products.count()

    context = {
        'products': page_obj,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):

    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(product=product, user=request.user)
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product=product, status=True)

    product_gallery = ProductGallery.objects.filter(product=product)
    
    context = {
        'product': product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    
    return render(request, 'store/product-detail.html', context)



def product_search(request):
    query = request.GET.get('query')
    products = []

    if query:
        products = Product.objects.filter(product_name__icontains=query) | Product.objects.filter(description__icontains=query)

    product_count = products.count()
    
    context = {
        'query': query,
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)



def submit_review(request, id):
    url = request.META.get('HTTP_REFERER')

    product = get_object_or_404(Product, id=id)
    user = request.user

    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user=user, product=product)
            form = ReviewForm(request.POST, instance=review)
            form.save()

            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)

            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user = user
                data.save()

                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)