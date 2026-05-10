from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('order_number', 'user__username', 'email')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'status', 'is_paid')}),
        ('Customer', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Address', {'fields': ('address', 'city', 'postal_code', 'country')}),
        ('Payment', {'fields': ('total_amount', 'payment_method')}),
    )
