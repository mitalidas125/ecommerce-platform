from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm

# ------------------------
# SIGNUP VIEW
# ------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('products:product_list')
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

# ------------------------
# LOGIN VIEW
# ------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'products:product_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

# ------------------------
# LOGOUT VIEW
# ------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('products:product_list')

# ------------------------
# PROFILE VIEW
# ------------------------
@login_required
def profile_view(request):
    user = request.user

    # Orders counts
    total_orders = user.orders.count()
    delivered_orders = user.orders.filter(status='delivered').count()
    pending_orders = user.orders.filter(status='pending').count()

    context = {
        'user': user,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }

    return render(request, 'users/profile.html', context)
