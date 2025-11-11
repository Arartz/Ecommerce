from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Homepage with products - requires authentication"""
    # Sample products data (in a real app, this would come from a database)
    products = [
        {
            'id': 1,
            'name': 'Wireless Headphones',
            'price': 79.99,
            'description': 'High-quality wireless headphones with noise cancellation',
            'image': '/static/images/headphones.jpg'
        },
        {
            'id': 2,
            'name': 'Smartphone',
            'price': 599.99,
            'description': 'Latest smartphone with advanced camera features',
            'image': '/static/images/smartphone.jpg'
        },
        {
            'id': 3,
            'name': 'Laptop',
            'price': 899.99,
            'description': 'Powerful laptop for work and gaming',
            'image': '/static/images/laptop.jpg'
        },
        {
            'id': 4,
            'name': 'Smart Watch',
            'price': 249.99,
            'description': 'Feature-rich smartwatch with health tracking',
            'image': '/static/images/smartwatch.jpg'
        }
    ]
    
    context = {
        'products': products,
        'user': request.user
    }
    return render(request, 'products/home.html', context)
