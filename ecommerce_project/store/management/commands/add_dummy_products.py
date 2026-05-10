from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Add dummy bakery products to the database'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Breads', 'description': 'Fresh artisan breads and loaves'},
            {'name': 'Pastries', 'description': 'Delicious pastries and croissants'},
            {'name': 'Cakes', 'description': 'Custom cakes for every occasion'},
            {'name': 'Cookies', 'description': 'Homemade cookies and biscuits'},
            {'name': 'Donuts', 'description': 'Fresh glazed and filled donuts'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': slugify(cat_data['name']), 'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))

        # Dummy products data
        products_data = [
            # Breads
            {'name': 'Sourdough Loaf', 'category': 'Breads', 'price': 5.99, 'stock': 20,
             'description': 'Authentic sourdough loaf with a crispy crust and tangy flavor'},
            {'name': 'Whole Wheat Bread', 'category': 'Breads', 'price': 4.99, 'stock': 25,
             'description': 'Nutritious whole wheat bread, perfect for breakfast'},
            {'name': 'French Baguette', 'category': 'Breads', 'price': 3.99, 'stock': 30,
             'description': 'Classic French baguette with a golden crust'},
            {'name': 'Ciabatta Roll', 'category': 'Breads', 'price': 2.49, 'stock': 40,
             'description': 'Soft Italian ciabatta roll, ideal for sandwiches'},

            # Pastries
            {'name': 'Croissant Butter', 'category': 'Pastries', 'price': 3.50, 'stock': 35,
             'description': 'Buttery French croissant with layers of deliciousness'},
            {'name': 'Almond Croissant', 'category': 'Pastries', 'price': 4.50, 'stock': 20,
             'description': 'Croissant topped with almond slices and cream'},
            {'name': 'Chocolate Eclair', 'category': 'Pastries', 'price': 4.99, 'stock': 25,
             'description': 'Elegant eclair filled with chocolate cream'},
            {'name': 'Strawberry Tart', 'category': 'Pastries', 'price': 5.99, 'stock': 15,
             'description': 'Fresh strawberry tart with custard filling'},

            # Cakes
            {'name': 'Chocolate Layer Cake', 'category': 'Cakes', 'price': 18.99, 'stock': 10,
             'description': 'Rich chocolate cake with creamy frosting'},
            {'name': 'Vanilla Cheesecake', 'category': 'Cakes', 'price': 16.99, 'stock': 8,
             'description': 'Smooth and creamy cheesecake with vanilla flavor'},
            {'name': 'Red Velvet Cake', 'category': 'Cakes', 'price': 17.99, 'stock': 12,
             'description': 'Classic red velvet cake with cream cheese frosting'},
            {'name': 'Lemon Drizzle Cake', 'category': 'Cakes', 'price': 15.99, 'stock': 14,
             'description': 'Moist lemon cake with tangy icing'},

            # Cookies
            {'name': 'Chocolate Chip Cookie', 'category': 'Cookies', 'price': 1.99, 'stock': 100,
             'description': 'Classic cookie loaded with chocolate chips'},
            {'name': 'Oatmeal Raisin Cookie', 'category': 'Cookies', 'price': 1.99, 'stock': 90,
             'description': 'Hearty oatmeal cookie with juicy raisins'},
            {'name': 'Peanut Butter Cookie', 'category': 'Cookies', 'price': 2.49, 'stock': 80,
             'description': 'Rich and creamy peanut butter cookie'},
            {'name': 'Sugar Cookie', 'category': 'Cookies', 'price': 1.49, 'stock': 120,
             'description': 'Sweet and simple sugar cookie'},

            # Donuts
            {'name': 'Glazed Donut', 'category': 'Donuts', 'price': 1.50, 'stock': 50,
             'description': 'Classic glazed donut, light and fluffy'},
            {'name': 'Chocolate Frosted Donut', 'category': 'Donuts', 'price': 1.99, 'stock': 45,
             'description': 'Chocolate frosted with sprinkles'},
            {'name': 'Strawberry Donut', 'category': 'Donuts', 'price': 2.25, 'stock': 30,
             'description': 'Fresh strawberry filled donut'},
            {'name': 'Boston Cream Donut', 'category': 'Donuts', 'price': 2.50, 'stock': 25,
             'description': 'Classic Boston cream filled donut'},
        ]

        # Add products
        created_count = 0
        for prod_data in products_data:
            category = categories[prod_data['category']]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'slug': slugify(prod_data['name']),
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                # Generate and save placeholder image
                if not product.image:
                    image = self.generate_placeholder_image(prod_data['name'])
                    product.image.save(
                        f"{slugify(prod_data['name'])}.png",
                        ContentFile(image),
                        save=True
                    )
                self.stdout.write(self.style.SUCCESS(f'✓ Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Product already exists: {product.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully added {created_count} dummy products!'))

    def generate_placeholder_image(self, product_name):
        """Generate a placeholder image with product name and bakery colors"""
        img = Image.new('RGB', (400, 300), color=(195, 121, 96))  # Bakery primary color
        draw = ImageDraw.Draw(img)
        
        # Add text to image
        text = product_name[:25]  # Limit text length
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (400 - text_width) // 2
        y = (300 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255))
        
        # Save to bytes
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io.getvalue()
