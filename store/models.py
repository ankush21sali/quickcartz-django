from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def averageReview(self):
        avg = 0
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        
        return avg
    
    def countReview(self):
        count = 0
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        if reviews['count'] is not None:
            count = int(reviews['count'])
        
        return count


COLOR_CHOICES = [
    ('Black', 'Black'),
    ('White', 'White'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Gray', 'Gray'),
]

SIZE_CHOICES = [
        ('XS','XS'),('S','S'),('M','M'),
        ('L','L'),('XL','XL'),('XXL','XXL')
    ]


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    # stock = models.IntegerField(default=0)
    # price = models.IntegerField(blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.product_name} ({self.color}, {self.size})"
    


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject