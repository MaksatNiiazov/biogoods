import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from parserInter.models import Product, ProductInOrder, Order, SiteInfo
from parserInter.forms import EmailForm, ProductForm
from user_auth.models import User


contact_info = SiteInfo.objects.get(id=1)


class ProfileView(TemplateView):
    template_name = 'parserInter/profile.html'

    def get_queryset(self):
        return User.objects.get(email=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = User.objects.get(email=self.request.user)
        
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'company', 'address']
    template_name = 'parserInter/profile_update.html'
    success_url = reverse_lazy('profile')


class MainPageView(ListView):
    model = Product
    template_name = 'parserInter/index.html'


class ProductListView(ListView):
    model = Product
    paginate_by = int(os.environ.get('PAGINATE_BY', 40))
    template_name = 'parserInter/products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'parserInter/product.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'parserInter/product_update.html'


class AddProductView(View):
    def post(self, request):
        order = Order.objects.get_or_create(user=self.request.user, status='pending', confirmed=False)
        order_id = Order.objects.get(user=self.request.user, status='pending', confirmed=False)
        product_id = Product.objects.get(id=int(self.request.POST.get('product'))).pk,
        product_price = Product.objects.get(id=int(self.request.POST.get('product'))).price
        count = int(self.request.POST.get('count')),
        total_price = product_price * count[0]
        product_in_order = ProductInOrder(
            order=order_id,
            product_id=product_id[0],
            count=count[0],
            total_price=total_price,
        )
        product_in_order.save()
        total_count = order_id.products_in_order.values('count')
        grand_total = order_id.products_in_order.values('total_price')
        order_id.items = sum(item['count'] for item in total_count)
        order_id.grand_total = sum(item['total_price'] for item in grand_total) - order_id.discount
        order_id.confirmed = False
        order_id.save()

        return redirect('product-list')


class ProductInOrderUpdateView(View, LoginRequiredMixin):
    model = ProductInOrder

    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        obj = ProductInOrder.objects.get(id=self.request.POST.get('obj_id'))
        order = Order.objects.get(user=self.request.user, status='pending', confirmed=False)
        order.grand_total = int(order.grand_total) - int(obj.total_price)
        order.items = int(order.items) - int(obj.count)
        obj.count = request.POST.get('count')
        obj.total_price = int(obj.product.price) * int(obj.count)
        order.grand_total = int(order.grand_total) + int(obj.total_price)
        order.items = int(order.items) + int(obj.count)
        obj.save()
        order.save()
        return JsonResponse({'success': True})


class DeleteFromOrderView(DetailView):
    model = ProductInOrder
    success_url = reverse_lazy('cart')
    template_name = 'parserInter/delete_confirm.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        pio = ProductInOrder.objects.get(id=self.object.pk)
        self.count = pio.count
        self.price = pio.total_price
        self.object.delete()
        self.check_order(pio.order_id)

        return redirect("cart")

    def check_order(self, order_id):
        order = Order.objects.get(id=order_id)
        order.items -= self.count
        order.grand_total -= self.price
        order.save()

        if not order.products_in_order.all():
            order.delete()


class AboutView(ListView):
    model = Product
    template_name = 'parserInter/about.html'


class CartView(ListView):
    model = Order
    template_name = 'parserInter/cart.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='pending', confirmed=False)


class ContactView(TemplateView):
    template_name = 'parserInter/contact.html'


class OrdersView(ListView):
    model = Order
    template_name = 'parserInter/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, confirmed=True)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'parserInter/delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result

    def get_success_url(self):
        messages.success(self.request, f'Your order #{self.object.id} has been deleted successfully!')
        return reverse_lazy('orders')


class RepeatOrderView(View):
    def get(self, request, *args, **kwargs):
        old_order = Order.objects.get(id=self.kwargs['pk'])
        new_order = Order.objects.create(
            user=old_order.user,
            items=old_order.items,
            subtotal=old_order.subtotal,
            tax=old_order.tax,
            discount=old_order.discount,
            grand_total=old_order.grand_total,
            confirmed=False,
            status='pending'
        )
        products = old_order.products_in_order.all()
        for product in products:
            new_pio = ProductInOrder.objects.create(
                order=new_order,
                product=product.product,
                count=product.count,
                total_price=product.total_price,
            )
        return redirect("cart")


class PersonalView(TemplateView):
    template_name = 'parserInter/personal.html'


def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'message': request.POST['message'],
            }
            html_body = render_to_string('email_templates/email.html', data)
            msg = EmailMultiAlternatives(subject='Message', to=[f'{contact_info.email}'])
            # print(f'{contact_info.email}')
            msg.attach_alternative(html_body, 'text/html')
            msg.send()

        return redirect('/')


def send_order(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            confirm_order = Order.objects.get(id=request.POST['order'])
            confirm_order.confirmed = True
            confirm_order.save()
            data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'message': request.POST['message'],
                'grand_total': request.POST['grand_total']
            }
            html_body = render_to_string('email_templates/order_email.html', data)
            msg = EmailMultiAlternatives(subject='Order', to=[f'{contact_info.email}'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()

        return redirect('orders')


class Login(LoginView):
    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url("home")
