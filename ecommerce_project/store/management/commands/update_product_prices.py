from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = 'Update product prices to Philippine Pesos (₱)'

    def handle(self, *args, **options):
        # Update prices with Philippine Pesos
        products = {
            'Sourdough Loaf': 150.00,
            'Whole Wheat Bread': 120.00,
            'French Baguette': 90.00,
            'Ciabatta Roll': 50.00,
            'Croissant Butter': 80.00,
            'Almond Croissant': 110.00,
            'Chocolate Eclair': 120.00,
            'Strawberry Tart': 150.00,
            'Chocolate Layer Cake': 550.00,
            'Vanilla Cheesecake': 480.00,
            'Red Velvet Cake': 520.00,
            'Lemon Drizzle Cake': 450.00,
            'Chocolate Chip Cookie': 45.00,
            'Oatmeal Raisin Cookie': 45.00,
            'Peanut Butter Cookie': 60.00,
            'Sugar Cookie': 35.00,
            'Glazed Donut': 35.00,
            'Chocolate Frosted Donut': 45.00,
            'Strawberry Donut': 55.00,
            'Boston Cream Donut': 65.00,
        }

        for product_name, price in products.items():
            Product.objects.filter(name=product_name).update(price=price)
            self.stdout.write(self.style.SUCCESS(f'✓ Updated {product_name} to ₱{price}'))

        self.stdout.write(self.style.SUCCESS('\n✓ All product prices updated successfully!'))
