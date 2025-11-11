from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.http import JsonResponse
from django.template.response import TemplateResponse

@login_required
def home(request):
    """Homepage with products - requires authentication"""
    # Get all products from database
    products = Product.objects.all()
    
    # Get cart item count for display
    cart_count = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = cart.get_item_count()
    except Cart.DoesNotExist:
        pass
    
    context = {
        'products': products,
        'user': request.user,
        'cart_count': cart_count
    }
    return render(request, 'products/home.html', context)

@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if item already exists in cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    # If item already exists, increment quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity to {cart_item.quantity}')
    else:
        messages.success(request, f'Added {product.name} to cart')
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count()
        })
    
    # Redirect back to home page or cart page for non-AJAX requests
    return redirect('home')

@login_required
def view_cart(request):
    """Display cart contents"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total = cart.get_total()
        cart_count = cart.get_item_count()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total = 0
        cart_count = 0
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count
    }
    return render(request, 'products/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from cart')
    return redirect('view_cart')

@login_required
def update_cart_quantity(request, item_id):
    """Update cart item quantity via AJAX"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'subtotal': float(cart_item.get_subtotal()),
                'total': float(cart_item.cart.get_total()),
                'cart_count': cart_item.cart.get_item_count()
            })
        else:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'removed': True,
                'total': float(cart_item.cart.get_total() if Cart.objects.filter(user=request.user).exists() else 0),
                'cart_count': Cart.objects.get(user=request.user).get_item_count() if Cart.objects.filter(user=request.user).exists() else 0
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def test_images(request):
    """Test view to debug image loading"""
    products = Product.objects.all()
    return TemplateResponse(request, 'test_images.html', {'products': products})

def product_detail(request, product_id):
    """Return product details and similar products via AJAX"""
    if request.method == 'GET':
        try:
            # Get the main product
            product = get_object_or_404(Product, id=product_id)
            
            # Get similar products (products with similar price range or name)
            from decimal import Decimal
            similar_products = Product.objects.exclude(id=product_id).filter(
                price__gte=product.price * Decimal('0.8'),  # Within 20% price range
                price__lte=product.price * Decimal('1.2')
            )[:6]  # Limit to 6 similar products
            
            # If not enough similar products by price, get random ones
            if similar_products.count() < 3:
                additional_products = Product.objects.exclude(id=product_id).exclude(
                    id__in=similar_products.values_list('id', flat=True)
                )[:3]
                similar_products = list(similar_products) + list(additional_products)
            
            # Prepare product data
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'image': product.image
            }
            
            # Prepare similar products data
            similar_products_data = []
            for similar_product in similar_products:
                similar_products_data.append({
                    'id': similar_product.id,
                    'name': similar_product.name,
                    'price': str(similar_product.price),
                    'image': similar_product.image
                })
            
            return JsonResponse({
                'success': True,
                'product': product_data,
                'similar_products': similar_products_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
