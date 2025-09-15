from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Category, Brand, Collection, Attribute,
    Product, ProductImage, ProductAttribute
)

# Admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('parent',)


# Admin configuration for Brand model
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url')
    search_fields = ('name', 'description')


# Admin configuration for Collection model
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


# Admin configuration for Attribute model
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Inline for ProductImage to be used within the Product admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Number of empty forms to display
    fields = ('image', 'alt_text', 'caption', 'display_order')


# Admin configuration for Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'is_published', 'date_created')
    list_filter = ('is_published', 'category', 'brand')
    search_fields = ('name', 'sku', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category', 'brand') # Use raw_id_fields for FKs to improve performance with many items
    filter_horizontal = ('collections',) # For Many-to-Many relationships
    readonly_fields = ('date_created', 'date_updated')
    inlines = [ProductImageInline]


# Admin configuration for ProductImage model (can be managed independently if needed)
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'display_order')
    list_filter = ('product',)
    search_fields = ('product__name', 'alt_text', 'caption')
    raw_id_fields = ('product',)


# Admin configuration for ProductAttribute model
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('get_attribute_name', 'value')
    filter_horizontal = ('product',) # For Many-to-Many with Product
    list_filter = ('attribute',)
    search_fields = ('attribute__name', 'value')

    def get_attribute_name(self, obj):
        return obj.attribute.name
    get_attribute_name.short_description = _('Attribute')
    get_attribute_name.admin_order_field = 'attribute__name'
