from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Category, ProductReview


def home(request):
    """Homepage with featured products."""
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
    })


def product_list(request, category_slug=None):
    """List all products, optionally filtered by category."""
    category = None
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
    })


def product_detail(request, slug):
    """Show product details with reviews."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


@method_decorator(login_required, name='dispatch')
class AddReviewView(View):
    """Add a review to a product."""
    
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        return render(request, 'store/product_detail.html', {
            'product': product,
            'message': 'Review added successfully!',
        })
