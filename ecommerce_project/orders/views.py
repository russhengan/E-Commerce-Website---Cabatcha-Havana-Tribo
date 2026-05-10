from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from uuid import uuid4
from cart.models import Cart, CartItem
from store.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    """Checkout page."""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart:cart_view')
    
    if not cart.items.exists():
        return redirect('cart:cart_view')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{uuid4().hex[:8].upper()}",
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            total_amount=cart.get_total_price(),
            payment_method=request.POST.get('payment_method', 'card'),
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
            
            # Reduce product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('orders:order_confirmation', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_history(request):
    """User's order history."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
