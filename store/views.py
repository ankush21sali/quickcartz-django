from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):

    category  = None
    products = None

    if category_slug != None:
        category  = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category , is_available=True)

    else:
        products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    
    context = {
        'product': product
    }
    
    return render(request, 'store/product-detail.html', context)