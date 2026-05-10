from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw
from store.models import Product


class Command(BaseCommand):
    help = 'Add placeholder images to existing products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            if not product.image:
                # Generate placeholder image
                image = self.generate_placeholder_image(product.name)
                product.image.save(
                    f"{slugify(product.name)}.png",
                    ContentFile(image),
                    save=True
                )
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Added image to: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Already has image: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully added {updated_count} images!'))

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
