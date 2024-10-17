from django.db import models

class Category(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    name = models.CharField(max_length=255, verbose_name="Category Name")
    image = models.ImageField(upload_to='categories/category/', verbose_name="Category Image", blank=True, null=True)
    description = models.TextField(verbose_name="Category Description", default="")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class ProductVideo(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='videos', verbose_name="Product")
    video = models.FileField(upload_to='products/videos/', verbose_name="Product Video", blank=True, null=True)

    class Meta:
        db_table = 'product_videos'

    def __str__(self):
        return f"Video for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    image = models.ImageField(upload_to='products/images/', verbose_name="Product Image")

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return f"Image for {self.product.name}"

class Product(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Category")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(verbose_name="Stock")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU Number")  # SKU number
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Status")  # Active/Inactive
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'products'
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
