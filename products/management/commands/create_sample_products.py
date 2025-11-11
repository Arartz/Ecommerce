"""
Management command to create sample products
Usage: python manage.py create_sample_products
"""
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Creates sample products for testing'

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and long battery life. Perfect for music lovers and professionals.',
                'price': 99.99,
                'image': '/static/images/headphones.jpg'
            },
            {
                'name': 'Laptop Computer',
                'description': 'Powerful laptop with latest processor, 16GB RAM, and 512GB SSD. Ideal for work and gaming.',
                'price': 1299.99,
                'image': '/static/images/laptop.jpg'
            },
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone with advanced camera, 5G connectivity, and all-day battery life.',
                'price': 799.99,
                'image': '/static/images/smartphone.jpg'
            },
            {
                'name': 'Smart Watch',
                'description': 'Feature-rich smartwatch with fitness tracking, heart rate monitor, and smartphone notifications.',
                'price': 249.99,
                'image': '/static/images/smartwatch.jpg'
            },
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_count} new product(s)')
        )

