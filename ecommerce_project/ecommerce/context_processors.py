from cart.models import Cart


def cart_processor(request):
    """Add cart information to template context."""
    cart_items = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.get_total_items()
        except Cart.DoesNotExist:
            pass
    return {'cart_items': cart_items}
