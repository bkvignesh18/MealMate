from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Restaurant, Item, Cart

# Create your views here.
def home(request):
    return render(request, 'delivery/index.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Customer.objects.get(username = username, password = password)
            if username == 'Admin':
                return render(request, 'delivery/admin_home.html')
            else:
                restaurant_list = Restaurant.objects.all()
                return render(request, 'delivery/customer_home.html', {'restaurantList': restaurant_list, 'username' : username})

        except Customer.DoesNotExist:
            return render(render, 'delivery/invalid_credentials.html')
        
    else:
        return render(request, 'delivery/signin.html')
    

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username = username)
            return HttpResponse("Username already exists.")

        except:
            Customer.objects.create(
                username = username,
                password = password,
                email = email,
                mobile = mobile,
                address = address,
            )
            return render(request, 'delivery/signin.html')
        
    else:
        return render(request, 'delivery/signup.html')
    
def customer_home(request, username):
    restaurant_list = Restaurant.objects.all()
    return render(request, 'delivery/customer_home.html', {'restaurantList': restaurant_list, 'username' : username})
        
def add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html')

def restaurant_success(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
    
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse('Restaurant already exists.')

        except:
            Restaurant.objects.create(
            name = name,
            image_url = image_url,
            cuisine =cuisine,
            rating = rating
            )
            return render(request, 'delivery/admin_home.html')
        
def show_restaurants(request):
    restaurant_list = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {'restaurantList' : restaurant_list})

def update_restaurant(request, id):
    restaurant = Restaurant.objects.get(id = id)

    if request.method == 'POST':
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.image_url = image_url
        restaurant.cuisine = cuisine
        restaurant.rating = rating
        restaurant.save()

        restaurantList = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurantList" : restaurantList})
    
    else:
        return render(request, 'delivery/update_restaurant.html', {'r' : restaurant})

def delete_restaurant(request, id):
    restaurant = Restaurant.objects.get(id = id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList})

def update_menu(request, id):
    restaurant = Restaurant.objects.get(id = id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        image_url = request.POST.get('image_url')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                image_url = image_url
            )

        return render(request, 'delivery/admin_home.html')
    
    else:
        itemList = restaurant.items.all()
        return render(request, 'delivery/update_menu.html',{"itemList" : itemList, "r" : restaurant})
    
def view_menu(request, id, username):
    restaurant = Restaurant.objects.get(id = id)
    itemList = restaurant.items.all()
    return render(request, 'delivery/customer_menu.html',{"itemList" : itemList, "username" : username})

def add_to_cart(request, id, username):
    item = Item.objects.get(id = id)
    customer = Customer.objects.get(username = username)

    cart, _ = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    return render(request, 'delivery/added_to_cart.html')

def view_cart(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html', {"itemList" : items, "total_price" : total_price, "username" : username})

def place_order(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()

    total_price = cart.total_price() if cart else 0

    if cart and total_price > 0:
        cart.items.clear()
        return render(request, 'delivery/order_summary.html', {
            'username' : username,
            'customer' : customer,
            'total_price' : total_price
        })
    