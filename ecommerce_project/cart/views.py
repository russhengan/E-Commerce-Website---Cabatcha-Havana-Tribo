from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from store.models import Product
from .models import Cart, CartItem


@login_required
def cart_view(request):
    """Display the shopping cart."""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart',
            'cart_total': str(cart.get_total_items())
        })
    
    return redirect('cart:cart_view')


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_view')


@login_required
@require_http_methods(["POST"])
def update_cart_quantity(request, item_id):
    """Update quantity of item in cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart:cart_view')


@login_required
def clear_cart(request):
    """Clear the entire cart."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
    except Cart.DoesNotExist:
        pass
    
    return redirect('cart:cart_view')
