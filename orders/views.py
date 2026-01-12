from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # If user is logged in, assign user to order
            if request.user.is_authenticated:
                order.user = request.user
            else:
                # For anonymous users, create a temporary user or handle differently
                from django.contrib.auth.models import User
                # You can create anonymous user or require login
                # For now, we'll require them to be logged in
                messages.warning(request, 'Please login to place an order.')
                return redirect('products:product_list')
            
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})