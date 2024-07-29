from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem, Recommendation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cartitem_set.all() if cart else []
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()
        return redirect('order_history')
    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

def get_recommendations(user):
    if not user.is_authenticated:
        return []
    recommendations = Recommendation.objects.filter(user=user).order_by('-score')[:5]
    return [rec.product for rec in recommendations]

@login_required
def profile(request):
    return render(request, 'shop/profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})