from django.contrib import admin
from .models import *

# Register your models here.
# inline 
class FeaturesInline(admin.StackedInline):
    model = ProductFeatures
    extra = 0


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'price', 'new_price']
    list_filter = ['created', 'updated', 'discount']
    inlines = [ImageInline, FeaturesInline]
