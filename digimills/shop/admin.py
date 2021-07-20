from django.contrib import admin
from .models import CartModel, ProductModel, Order, CustomerModel
# Register your models here.
 

@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','house_number', 'street', 'locality', 'district', 'state'] 

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_category', 'product_brand', 'title', 'desc', 'market_price', 'selling_price','img'] 

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','product_id', 'user_id']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'customer', 'quantity', 'order_date', 'status']
