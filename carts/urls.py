from django.urls import path
from .import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("add_quantity/<int:product_id>/<int:variant_id>/", views.add_quantity, name="add_quantity"),
    path("remove_quantity/<int:product_id>/<int:variant_id>/", views.remove_quantity, name="remove_quantity"),
    path("remove_cart_item/<int:product_id>/<int:variant_id>/", views.remove_cart_item, name="remove_cart_item"),

    path('checkout/', views.checkout, name='checkout'),
]
