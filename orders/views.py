import logging
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .helpers import apology
from .models import Item, Pricing, Topping, Cart, CartItem

logger = logging.getLogger(__name__)


def index(request):
    """
    Render the index page
    """
    return render(request, template_name="index.html")


def load(request):
    """
    Send the menuitems to the front end as json
    """
    menu_items = Item.objects.all()

    # res is a dictionary that should represent the menu.
    # Each key of the dictionary represents a menu category.
    # The value of each key is a list that contains dictionaries
    # that contain details about the menuitem itself, price and as such.
    # Below is an example
    # {
    #   'Regular pizza': [{'name': 'Cheese'},
    #                    {'name': 'One topping'}]
    #    'Sub': [{'name': 'Ham and Cheese'},
    #           {'name': 'Eggplant Parmigiana'}]
    # }
    res = dict()
    for item in menu_items:
        if item.category.name in res:
            res[item.category.name].append({
                'name': item.__str__(),
                'id': item.id,
            })
        else:
            res[item.category.name] = [
                {
                    'name': item.__str__(),
                    'id': item.id,
                }
            ]
    response_data = {'menu': res}
    return JsonResponse(response_data)


def login_user(request):
    """
    Implement user login
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # User authenticated
            request.session['user_id'] = user.id
            login(request, user=user)
            return redirect(index)
        else:
            return apology(request, "Username or password are not correct")
    else:
        return render(request, template_name="login.html")


def register(request):
    """
    Implement user registration
    """
    if request.method == 'POST':
        username = request.POST.get('username')

        # check if thus user name is already taken
        # if yes render error template
        user = User.objects.filter(username=username)
        if user:
            return apology(request, message="username already taken")

        # check if password and confirmation match
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            return apology(request, message="password and confirmation "
                                            "do not match")

        # create user and store in database
        User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        request.session['user_id'] = user.id
        login(request, user=user)
        return redirect(index)

    else:
        return redirect(register)


def logout_user(request):
    """
    Log user out
    """
    logout(request)
    return redirect(login_user)


def get_item(request, id):
    """
    Get item details and pass it on
    """
    item = Item.objects.filter(id=id)
    toppings = [t for t in Topping.objects.all().
                values_list('name', flat=True)]
    # get all pricings for this item
    pricings = Pricing.objects.filter(item=item[0])

    # list to store pricings as a list that contains
    # lists
    res = []
    for pricing in pricings:
        res.append([pricing.pricing_type, pricing.price, pricing.id])

    item_data = {
        'name': item[0].__str__(),
        'max_toppings': item[0].max_toppings,
        'pricing': res,
        'toppings': toppings
    }
    response_data = {'item': item_data}
    return JsonResponse(response_data)


@csrf_exempt
def checkout(request):
    """
    Implement user checkout
    """
    logger.warning("In the checkout method")
    data = request.POST['orders']
    logger.warning("Data: " + data)

    # order_items is a list of dictionaries, each dictionary has
    # three keys, listed below
    # - id: id of the item
    # - toppings: a list of toppings, if no toppings an empty list
    # - size: the size of the item
    # - price: price of an item
    # below is an example
    # [
    #    {"toppings": ["Pepperoni"], "size": "small",
    #     "name": "Regular Two topping Pizza", "price": "15.20", "id": "3"},
    #
    #    {"toppings": ["Sausage", "Eggplant"], "size": "small",
    #     "name": "Sicilian Two topping Pizza", "price": "15.20", "id": "3"}
    # ]
    order_items = json.loads(data)

    # create cart
    cart = Cart.objects.create()

    # loop over all order_items and create cart items
    for order_item in order_items:
        pricing_id = order_item['pricing_id']
        pricing = Pricing.objects.filter(id=pricing_id)
        cart_item = CartItem.objects.create(cart=cart, pricing=pricing[0])
        logger.warning("New cart item: "+ cart_item)
