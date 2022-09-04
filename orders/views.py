import imp
from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
from home.models import Product
from .forms import CartAddForms
from .models import Order, OrderItem



class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})

class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForms(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)
class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order':order})