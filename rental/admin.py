from django.contrib import admin
from .models import Category, Equipment, Booking


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price_per_day',
        'quantity_total',
        'quantity_available',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price_per_day', 'quantity_available', 'is_active')
    readonly_fields = ('created_at',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'equipment',
        'start_date',
        'end_date',
        'total_price',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at', 'start_date')
    search_fields = ('user__username', 'equipment__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'