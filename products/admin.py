from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Cart, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'image_preview']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Product Image', {
            'fields': ('image',),
            'description': 'Enter the image URL or path. For static images, use: /static/images/filename.jpg. You can also use external URLs.'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Image Preview'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'get_item_count', 'get_total']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Item Count'
    
    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'get_subtotal', 'added_at']
    list_filter = ['added_at']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['added_at']
    
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'
