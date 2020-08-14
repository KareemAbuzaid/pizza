from django.contrib import admin
from .models import Category, Pricing, Item, Topping, Cart, CartItem


admin.site.register(Category)
admin.site.register(Pricing)
admin.site.register(Item)
admin.site.register(Topping)
admin.site.register(Cart)
admin.site.register(CartItem)