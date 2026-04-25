from django.contrib import admin
from .models import Category, Sight


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Sight)
class SightAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'address', 'views_count', 'created_at']
    list_filter = ['category', 'created_at']
    readonly_fields = ['views_count']
    exclude = ('views_count',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'short_description', 'full_description')
        }),
        ('Локация', {
            'fields': ('address',)
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Дополнительно', {
            'fields': ('opening_hours', 'ticket_price', 'views_count')
        }),
    )
