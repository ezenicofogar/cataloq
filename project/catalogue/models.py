from django.db import models
from django.utils.translation import gettext_lazy as _

# --- Core Catalogue Models ---

class Category(models.Model):
    """
    Represents a product category. Categories can be nested to create a hierarchy.
    """
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        help_text=_("The name of the category.")
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True,
        help_text=_("A unique, URL-friendly version of the name.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("A short description of the category.")
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_("Parent Category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text=_("Assign a parent to create a category hierarchy.")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self):
        # Create a breadcrumb-style path for nested categories
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Brand(models.Model):
    """
    Represents a product brand or manufacturer.
    """
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
        help_text=_("The name of the brand.")
    )
    logo = models.ImageField(
        verbose_name=_("Logo"),
        upload_to='brand',
        blank=True,
        null=True,
        help_text=_("The brand's logo image.")
    )
    website_url = models.URLField(
        verbose_name=_("Website URL"),
        blank=True,
        help_text=_("The official website of the brand.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("A brief description of the brand.")
    )

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ['name']

    def __str__(self):
        return self.name


class Collection(models.Model):
    """
    Represents a curated collection of products (e.g., "Summer Collection").
    """
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ['name']

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Represents a type of product attribute (e.g., 'Color', 'Size', 'Material').
    """
    name = models.CharField(
        verbose_name=_("Attribute Name"),
        max_length=100,
        unique=True,
        help_text=_("e.g., Color, Size, Material")
    )

    class Meta:
        verbose_name = _("Attribute")
        verbose_name_plural = _("Attributes")
        ordering = ['name']

    def __str__(self):
        return self.name

# --- Product and Related Models ---

class Product(models.Model):
    """
    The main product model.
    """
    name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=255
    )
    sku = models.CharField(
        verbose_name=_("SKU (Stock Keeping Unit)"),
        max_length=100,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )
    short_description = models.TextField(
        verbose_name=_("Short Description"),
        blank=True,
        help_text=_("A brief summary of the product.")
    )
    is_published = models.BooleanField(
        verbose_name=_("Is Published"),
        default=False,
        help_text=_("Check this to make the product visible on the site.")
    )
    date_created = models.DateTimeField(
        verbose_name=_("Date Created"),
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        verbose_name=_("Date Updated"),
        auto_now=True
    )

    # --- Relationships ---
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.PROTECT,  # Prevents deleting a category with products
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name=_("Brand"),
        on_delete=models.SET_NULL, # Products can exist without a brand
        null=True,
        blank=True,
        related_name='products'
    )
    collections = models.ManyToManyField(
        Collection,
        verbose_name=_("Collections"),
        blank=True,
        related_name='products'
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-date_created']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    An image associated with a specific product.
    """
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE, # If product is deleted, its images are too
        related_name='images'
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to='product',
        help_text=_("The product image file.")
    )
    alt_text = models.CharField(
        verbose_name=_("Alt Text"),
        max_length=255,
        help_text=_("Descriptive text for SEO and accessibility.")
    )
    caption = models.CharField(
        verbose_name=_("Caption"),
        max_length=255,
        blank=True
    )
    display_order = models.PositiveIntegerField(
        verbose_name=_("Display Order"),
        default=0,
        help_text=_("The order in which to display images (0 comes first).")
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['display_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"


class ProductAttribute(models.Model):
    """
    A specific attribute value for products (e.g., Product: 'T-Shirt', Attribute: 'Color', Value: 'Red').
    """
    product = models.ManyToManyField(
        Product,
        verbose_name=_("Product"),
        blank=True,
        related_name='attributes'
    )
    attribute = models.ForeignKey(
        Attribute,
        verbose_name=_("Attribute"),
        on_delete=models.CASCADE # If an attribute type is deleted, so are its values
    )
    value = models.CharField(
        verbose_name=_("Value"),
        max_length=255,
        help_text=_("The specific value for the attribute (e.g., Red, Large).")
    )

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        ordering = ['attribute__name']

    def __str__(self):
        return f"{self.product.name}: {self.attribute.name} - {self.value}"
