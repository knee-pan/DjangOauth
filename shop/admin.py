from django.contrib import admin

from shop.models import Category, Product

# admin.site.register(Category)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("is_active",)
    search_fields = ("title",)
