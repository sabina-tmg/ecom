from django.shortcuts import render,redirect
from .models import * 
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponse
from django.urls import reverse
from hashlib import sha256
from django.shortcuts import render, get_object_or_404


def home(request):
    date=datetime.now()
    products = Product.objects.filter(status='publish') 
    banners = Banner.objects.all()
    context = {
        'products': products,
        'banners':banners,
        'date':date,

    }
    
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')
def account(request):
    return render(request,'main/account.html')

    
def product(request):
    categories=Categories.objects.all()
    filter_price=Filter_price.objects.all()
    color=Color.objects.all()
    brand=Brand.objects.all()
    
    CAT_ID = request.GET.get('categories')
    filter_price_id = request.GET.get('filter_price')
    Color_id=request.GET.get('color')
    Brand_id=request.GET.get('brand')
    ATOZ_id=request.GET.get('ATOZ')
    ZTOA_id=request.GET.get('ZTOA')
    PRICE_LOWTOHIGH_id=request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW_id=request.GET.get('PRICE_HIGHTOLOW')
    New_Product_id=request.GET.get('New_product')
    old_Product_id=request.GET.get('Old_product')


    if CAT_ID:
       products = Product.objects.filter(categories=CAT_ID, status='publish')
    elif filter_price_id:
        products = Product.objects.filter(filter_price=filter_price_id, status='publish')
    elif Color_id:
        products=Product.objects.filter(color=Color_id,status='publish')
    elif Brand_id:
        products=Product.objects.filter(brand=Brand_id,status='publish')
    elif ATOZ_id:
        products=Product.objects.filter(status="publish").order_by('name')
    elif ZTOA_id:
        products=Product.objects.filter(status="publish").order_by('-name')
    elif PRICE_LOWTOHIGH_id:
        products=Product.objects.filter(status="publish").order_by('price')
    elif PRICE_HIGHTOLOW_id:
        products=Product.objects.filter(status="publish").order_by('-price')
    elif New_Product_id:
        products=Product.objects.filter(status="publish",condition="New").order_by('-id')
    elif old_Product_id:
        products=Product.objects.filter(status="publish",condition='Old').order_by('-id')
                       
    else:
      products = Product.objects.filter(status='publish').order_by('-id')

    
    
    context = {
        'products': products,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand
    }
    return render(request, 'main/product.html', context)


def search(request):
    search_query = request.GET.get('searched', '')
    product = Product.objects.filter(name__icontains=search_query)

    context = {
        'product': product
    }
    return render(request, 'main/search.html', context)

def product_detail(request,id):
    product = Product.objects.filter(id=id).first()
    context = {
        'product': product
    }
    return render(request, 'main/product_single.html', context)


date=datetime.now()
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save contact message to the database
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        # Prepare email details
        email_subject = 'Electronic Platform'
        email_message = render_to_string('main/msg.html',{'name':name,'date':date})
        from_email = 'syangtansabina8@gmail.com'
        recipient_list = [email]
        fail_silently = False

        # Send email
        send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=False)

        # Success message
        messages.success(request, f'Hi {name}, your message has been successfully submitted!Please check your mail')

        return redirect('contact')

    return render(request, 'main/contact.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email address already exists")
            else:
                User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, "Registration successful!")
                return redirect('log_in')
        else:
            messages.error(request, "Passwords do not match")
        
    return render(request, 'auth/registration.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username is not registered yet!")
            return redirect('log_in')  # Redirect back to login if the username doesn't exist
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('log_in')  # Redirect back to login if authentication fails

    return render(request, 'auth/registration.html')


def log_out(request):
    logout(request)
    return redirect('home')


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def checkout(request):

    
    return render(request,'cart/checkout.html')


def payment(request):
    return render(request,'payments/esewa.html')

def success(request):
    return render(request,'cart/thank_you.html')





def place_order(request):
    if request.method == 'POST':
        # Retrieve user ID from session
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        
        # Retrieve form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address_line1 = request.POST.get('address_line1', '')
        address_line2 = request.POST.get('address_line2', '')
        address = f"{address_line1} {address_line2}".strip()
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        # Validation for empty fields and phone length
        if not all([firstname, lastname, country, address, city, state, postcode, phone, email, amount]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('checkout') 
        
        if len(phone) > 15:  # Adjust this limit as needed
            messages.error(request, "Phone number is too long.")
            return redirect('checkout')

        # Create a new order object
        order = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            amount=amount,
            payment_id=order_id,
        )

        # Save the order to the database
        order.save()
        for i in cart:
            a=(int(cart[i]['price']))
            b=cart[i]['quantity']
            total=a*b
            
            item=OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total_price=total
            )
            item.save()
        return redirect('place_order')  # Adjust URL as needed

    return render(request, 'cart/place_order.html')



def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    # Retrieve all orders related to the user
    orders = OrderItem.objects.filter(user=user)
    print(orders)

    context = {
        'orders': orders,
    }

    return render(request, 'cart/my_order.html', context)

def blog_single_left(request):
    return render(request,'sidebar/blog_single_left.html')
def blog_single_right(request):
    return render(request,'sidebar/blog_single_right.html')

def shop_left_sidebar(request):
    return render(request,'sidebar/shop_left_sidebar.html')


def single_product(request,id):
    product = Product.objects.get(id=id)
    context={
        'product': product,
        
    }

    
    return render(request, 'main/single_product.html',context)

def compare(request):
    product=Product.objects.all()
    context={
        'product':product
    }
    return render(request,'main/compare.html',context)