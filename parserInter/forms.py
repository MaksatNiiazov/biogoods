from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from parserInter.models import Product, Order, ProductInOrder, SiteInfo


class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=100, min_length=2)
    last_name = forms.CharField(max_length=100, min_length=2)
    email = forms.EmailField()
    message = forms.CharField(max_length=3000)


class EmailOrderForm(forms.Form):
    first_name = forms.CharField(max_length=100, min_length=2)
    last_name = forms.CharField(max_length=100, min_length=2)
    phone_number = forms.CharField(max_length=20, min_length=2)
    email = forms.EmailField()
    message = forms.CharField(max_length=3000)
    grand_total = forms.CharField(max_length=10)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'user',
            'items',
            'subtotal',
            'tax',
            'discount',
            'grand_total',
        )


class SiteAdminForm(forms.ModelForm):
    about_main_content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = SiteInfo
        fields = '__all__'