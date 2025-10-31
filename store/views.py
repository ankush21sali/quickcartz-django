from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator

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

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    
    context = {
        'product': product,
        'in_cart': in_cart
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