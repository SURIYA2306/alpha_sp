from django.contrib import admin
from .models import Product, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at') 
    search_fields = ('name', 'description')  
    list_filter = ('created_at',) 

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at') 

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)


