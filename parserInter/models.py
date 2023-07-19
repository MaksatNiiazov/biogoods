from PIL import Image
from django.db import models
from datetime import date

from django.urls import reverse
from django.db.models import Sum

from user_auth.models import User
# Create your models here.


class SiteInfo(models.Model):
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    instagram_link = models.CharField(max_length=150, blank=True)
    facebook_link = models.CharField(max_length=150, blank=True)
    yelp_link = models.CharField(max_length=150, blank=True)
    company_info = models.TextField(blank=True)
    main_header = models.TextField(blank=True)
    main_header_content = models.TextField(blank=True)
    main_about = models.TextField(blank=True)
    main_content_1 = models.TextField(blank=True)
    main_content_2 = models.TextField(blank=True)
    main_products = models.TextField(blank=True)
    about_title = models.TextField(blank=True)
    about_content = models.TextField(blank=True)
    about_products_title = models.TextField(blank=True)
    about_products_content = models.TextField(blank=True)
    about_main_content = models.TextField(blank=True)
    products_content = models.TextField(blank=True)
    contact_page_content = models.TextField(blank=True)
    cart_info_cart = models.TextField(blank=True)

    def __str__(self):
        return f'Site Information'


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    material = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} / {self.count}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={"pk": self.id})


class Img(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=f'media/photos/{date.today()}')

    def __str__(self):
        return f'{self.product}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.img.path)

        image = image.resize((1000, 1000))

        image.save(self.img.path)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('finished', 'Finished'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    created_date = models.DateTimeField(auto_now=True)
    items = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    confirmed = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10)


    class Meta:
        ordering = ('-id', 'status', 'created_date')

    def __str__(self):
        return f'{self.user}, {self.created_date}'

    def items_sum(self):
        return self.objects.annotate(Sum('products_in_order__count'))


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products_in_order')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    count = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)


