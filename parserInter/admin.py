from django.contrib import admin
from parserInter.forms import SiteAdminForm
from parserInter.models import *
from django.utils.safestring import mark_safe


class ImgInLine(admin.StackedInline):
    model = Img
    readonly_fields = ("image",)
    list_display = ('img', 'image', )
    extra = 1

    @staticmethod
    def image(obj):
        return mark_safe(f'<img src = {obj.img.url} with = "100" height = "100"')


class ProductInOrder(admin.StackedInline):
    model = ProductInOrder
    extra = 0


@admin.register(Product)
class Product(admin.ModelAdmin):
    model = Product
    list_display = ("title", 'count', 'price', "material", "weight", 'length', 'width', 'height', 'in_stock',)
    list_editable = ('in_stock', )
    inlines = [ImgInLine, ]

    @staticmethod
    def get_image(obj):
        return mark_safe(f'<img src = {obj.images.img.url} with = "50" height = "60"')


@admin.register(Order)
class Order(admin.ModelAdmin):
    model = Order
    list_display = ("id", "user", 'created_date', 'items', "subtotal", "tax", 'discount', 'grand_total', 'status',)
    list_editable = ('status', )
    search_fields = ("user",)
    list_filter = ("user", "status")
    inlines = [ProductInOrder,]


@admin.register(SiteInfo)
class SiteInfo(admin.ModelAdmin):
    exclude = ('id', )
    form = SiteAdminForm


admin.site.register(Img)
