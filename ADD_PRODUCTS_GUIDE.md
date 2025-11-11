# How to Add Products to MiEL E-commerce

## Method 1: Using Django Admin (Easiest - Recommended)

### Step 1: Create a Superuser (if you don't have one)
```bash
cd MiEL
python manage.py createsuperuser
```
Follow the prompts to create your admin account (username, email, password).

### Step 2: Start the Development Server
```bash
python manage.py runserver
```

### Step 3: Access Admin Panel
1. Open your browser and go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Click on "Products" under the "PRODUCTS" section
4. Click "Add Product" button (top right)

### Step 4: Fill in Product Details
- **Name**: Enter the product name (e.g., "Wireless Mouse")
- **Description**: Enter a detailed description
- **Price**: Enter the price (e.g., 29.99)
- **Image**: Enter the image path. Options:
  - For static images: `/static/images/filename.jpg`
  - For external URLs: `https://example.com/image.jpg`
  - Leave blank if no image (placeholder will be used)

### Step 5: Save
Click "Save" to add the product to your store.

---

## Method 2: Using Django Shell

### Step 1: Open Django Shell
```bash
cd MiEL
python manage.py shell
```

### Step 2: Create a Product
```python
from products.models import Product

# Create a new product
product = Product.objects.create(
    name="Wireless Mouse",
    description="Ergonomic wireless mouse with long battery life and precision tracking.",
    price=29.99,
    image="/static/images/mouse.jpg"  # Optional
)

print(f"Created product: {product.name}")
```

### Step 3: Exit Shell
```python
exit()
```

---

## Method 3: Using Management Command (Bulk Create)

### Step 1: Run the Sample Products Command
```bash
cd MiEL
python manage.py create_sample_products
```

This will create sample products if they don't already exist.

### Step 2: Customize the Command
Edit `MiEL/products/management/commands/create_sample_products.py` to add your own products.

---

## Available Static Images

You have these images available in `MiEL/static/images/`:
- `headphones.jpg`
- `laptop.jpg`
- `placeholder.jpg`
- `placeholder.svg`
- `smartphone.jpg`
- `smartwatch.jpg`

To use them, enter: `/static/images/filename.jpg` in the image field.

---

## Adding Your Own Images

1. Place your image file in `MiEL/static/images/` directory
2. Use the path: `/static/images/your-image.jpg` in the product image field
3. Or use an external URL: `https://example.com/your-image.jpg`

---

## Tips

- Product images are optional - if left blank, a placeholder will be shown
- You can edit products anytime through the admin panel
- Products are displayed on the home page automatically
- The image preview in admin shows a thumbnail of the product image

