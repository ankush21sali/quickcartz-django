from django.db import models
from store.models import Product, ProductVariant

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    # def sub_total(self):
    #     # Future-proof subtotal
    #     return (self.variant.product.price if self.variant else self.product.price) * self.quantity

    def __str__(self):
        if self.variant:
            return f"{self.product.product_name} ({self.variant.color}, {self.variant.size})"
        return self.product.product_name