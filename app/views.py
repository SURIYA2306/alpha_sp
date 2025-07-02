from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from .models import Product, Cart, Order, OrderItem, Profile
from .forms import RegisterForm, ProfileForm, OrderStatusForm
from django.contrib.auth.models import User


# Home
def home(request):
    return render(request, 'app/home.html')


# Products listing and search
def products(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'app/products.html', {'products': products})


# Product details
def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'app/detail.html', {'product': product})


# Cart views
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'app/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'error': 'Your cart is empty.' if not cart_items else None
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, _ = Cart.objects.get_or_create(user=request.user, product=product)
    if cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.name} added to cart.")
    else:
        messages.error(request, "Not enough stock available.")
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart')


# Authentication
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('account')
        messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})


def logout_confirm(request):
    return render(request, 'app/logout_confirm.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('logout_confirm')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})


def forgot_password(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            message = "Password reset instructions sent to your email."
        except User.DoesNotExist:
            message = "Email address not found."
    return render(request, 'app/forgot_password.html', {'message': message})


# Profile
@login_required
def account_view(request):
    profile = request.user.profile
    return render(request, 'app/account.html', {'profile': profile})


@login_required
def update_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'app/update_profile.html', {'form': form})


# Orders
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    order.calculate_total()
    cart_items.delete()

    return redirect('order_success', order_id=order.id)


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        # ✅ Use correct field names from Order model
        order = Order.objects.create(
            user=request.user,
            shipping_name=request.POST.get("name"),
            address=request.POST.get("address"),
            phone=request.POST.get("phone"),
            shipping_pincode=request.POST.get("pincode"),
            payment_method=request.POST.get("payment_method"),
            payment_status='pending',
        )
        order.products.add(product)
        order.total_amount = product.price
        order.save()

        # ✅ Remove from cart if it exists
        Cart.objects.filter(user=request.user, product=product).delete()

        # ✅ Redirect to payment page
        return redirect('payment_page', order_id=order.id)

    # For GET request: show checkout page
    profile = Profile.objects.get(user=request.user)
    return render(request, 'app/checkout.html', {"product": product, "profile": profile})



@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id', '')  # optional
        order.payment_method = method
        order.payment_status = 'success'
        order.status = 'processing'
        order.save()
        return redirect('order_success', order_id=order.id)

    return render(request, 'app/payment.html', {'order': order})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'app/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/order_history.html', {'orders': orders})



# Admin order status update
@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.id} status updated.")
            return redirect('order_history')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'app/update_order_status.html', {'form': form, 'order': order})

def contact_view(request):
    return render(request, 'app/contact.html')
