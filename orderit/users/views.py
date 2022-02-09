from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.db.models import Q
from .models import *
from .forms import UpdateUserForm,UpdateProfileForm

#### ---------- General Side -------------------#####

# Showing index page
def index(request):
    return render(request, 'users/index.html', {})


# logout
def Logout(request):
    logout(request)
    return redirect("index")


#### -----------------Customer Side---------------------- ######

# Creating Customer Account
def customerRegister(request):
    form = CustomerSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.is_customer = True
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("ccreate")
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)


# Customer Login

def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.user_role.name == 'user':
                login(request, user)
                return redirect("index")
            else:
                login(request, user)
                return redirect("dashboard")
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'users/login.html')


def Signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomSignupForm()
    return render(request, 'users/signup.html', {'form': form})


# customer profile view
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'users/profile.html', {'user_form': user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')


"""# Create customer profile
def createCustomer(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("profile")
    context = {
        'form': form,
        'title': "Complete Your profile"
    }
    return render(request, 'users/profile_form.html', context)
"""

"""#  Update customer detail
def updateCustomer(request, id):
    form = CustomerForm(request.POST or None, instance=request.user.customer)
    if form.is_valid():
        form.save()
        return redirect('profile')
    context = {
        'form': form,
        'title': "Update Your profile"
    }
    return render(request, 'users/profile_form.html', context)
"""

"""@login_required(login_url='/login/user/')
def checkout(request, oii=None):
    if request.POST:
        addr = request.POST['address']
        ordid = request.POST['oid']
        Order.objects.filter(id=int(ordid)).update(delivery_addr=addr,
                                                   status=Order.ORDER_STATE_PLACED)
        return redirect('/orderplaced/')
    else:
        cart = request.COOKIES['cart'].split(",")
        cart = dict(Counter(cart))
        items = []
        totalprice = 0
        uid = CustomUser.objects.filter(username=request.user)
        oid = Order()
        oid.orderedBy = uid[0]
        for x, y in cart.items():
            item = []
            it = Menu.objects.filter(id=int(x))
            if len(it):
                oiid = orderItem()
                oiid.item_id = it[0]
                oiid.quantity = int(y)
                oid.r_id = it[0].r_id
                oid.save()
                oiid.ord_id = oid
                oiid.save()
                totalprice += int(y) * it[0].price
                item.append(it[0].item_id.fname)
                it[0].quantity = it[0].quantity - y
                it[0].save()
                item.append(y)
                item.append(it[0].price * int(y))

            items.append(item)
        oid.total_amount = totalprice
        oid.save()
        context = {
            "items": items,
            "totalprice": totalprice,
            "oid": oid.id
        }
        return render(request, 'users/order.html', context)

"""


####### ------------------- Restaurant Side ------------------- #####

# creating restuarant account
def restRegister(request):
    form = RestuarantSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.is_restaurant = True
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("rcreate")
    context = {
        'form': form
    }
    return render(request, 'users/restsignup.html', context)


# restuarant login
def restLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("rprofile")
            else:
                return render(request, 'users/restlogin.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'users/restlogin.html', {'error_message': 'Invalid Login'})
    return render(request, 'users/restlogin.html')


# restaurant profile view
def restaurantProfile(request, pk=None):
    if pk:
        user = CustomUser.objects.get(pk=pk)
    else:
        user = request.user

    return render(request, 'users/rest_profile.html', {'user': user})


"""# create restaurant detail
@login_required(login_url='/login/restaurant/')
def createRestaurant(request):
    form = RestuarantForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("rprofile")
    context = {
        'form': form,
        'title': "Complete Your Restaurant profile"
    }
    return render(request, 'users/rest_profile_form.html', context)

"""
"""# Update restaurant detail
@login_required(login_url='/login/restaurant/')
def updateRestaurant(request, id):
    form = RestuarantForm(request.POST or None, request.FILES or None, instance=request.user.restaurant)
    if form.is_valid():
        form.save()
        return redirect('rprofile')
    context = {
        'form': form,
        'title': "Update Your Restaurant profile"
    }
    return render(request, 'users/rest_profile_form.html', context)
"""

# add  menu item for restaurant
"""@login_required(login_url='/login/restaurant/')
def menuManipulation(request):
    if not request.user.is_authenticated:
        return redirect("rlogin")

    rest = Restaurant.objects.filter(id=request.user.restaurant.id);
    rest = rest[0]
    if request.POST:
        type = request.POST['submit']
        if type == "Modify":
            menuid = int(request.POST['menuid'])
            memu = Menu.objects.filter(id=menuid). \
                update(price=int(request.POST['price']), quantity=int(request.POST['quantity']))
        elif type == "Add":
            itemid = int(request.POST['item'])
            item = Item.objects.filter(id=itemid)
            item = item[0]
            menu = Menu()
            menu.item_id = item
            menu.r_id = rest
            menu.price = int(request.POST['price'])
            menu.quantity = int(request.POST['quantity'])
            menu.save()
        else:
            menuid = int(request.POST['menuid'])
            menu = Menu.objects.filter(id=menuid)
            menu[0].delete()

    menuitems = Menu.objects.filter(r_id=rest)
    menu = []
    for x in menuitems:
        cmenu = []
        cmenu.append(x.item_id)
        cmenu.append(x.price)
        cmenu.append(x.quantity)
        cmenu.append(x.id)
        menu.append(cmenu)

    menuitems = Item.objects.all()
    items = []
    for y in menuitems:
        citem = []
        citem.append(y.id)
        citem.append(y.fname)
        items.append(citem)

    context = {
        "menu": menu,
        "items": items,
        "username": request.user.username,
    }
    return render(request, 'menu/menu_modify.html', context)
"""
"""
def orderlist(request):
    if request.POST:
        oid = request.POST['orderid']
        select = request.POST['orderstatus']
        select = int(select)
        order = Order.objects.filter(id=oid)
        if len(order):
            x = Order.ORDER_STATE_WAITING
            if select == 1:
                x = Order.ORDER_STATE_PLACED
            elif select == 2:
                x = Order.ORDER_STATE_ACKNOWLEDGED
            elif select == 3:
                x = Order.ORDER_STATE_COMPLETED
            elif select == 4:
                x = Order.ORDER_STATE_DISPATCHED
            elif select == 5:
                x = Order.ORDER_STATE_CANCELLED
            else:
                x = Order.ORDER_STATE_WAITING
            order[0].status = x
            order[0].save()

    orders = Order.objects.filter(r_id=request.user.restaurant.id).order_by('-timestamp')
    corders = []

    for order in orders:

        user = CustomUser.objects.filter(id=order.orderedBy.id)
        user = user[0]
        corder = []
        if user.is_restaurant:
            corder.append(user.restaurant.rname)
            corder.append(user.restaurant.info)
        else:
            corder.append(user.customer.f_name)
            corder.append(user.customer.phone)
        items_list = orderItem.objects.filter(ord_id=order)

        items = []
        for item in items_list:
            citem = []
            citem.append(item.item_id)
            citem.append(item.quantity)
            menu = Menu.objects.filter(id=item.item_id.id)
            citem.append(menu[0].price * item.quantity)
            menu = 0
            items.append(citem)

        corder.append(items)
        corder.append(order.total_amount)
        corder.append(order.id)

        x = order.status
        if x == Order.ORDER_STATE_WAITING:
            continue
        elif x == Order.ORDER_STATE_PLACED:
            x = 1
        elif x == Order.ORDER_STATE_ACKNOWLEDGED:
            x = 2
        elif x == Order.ORDER_STATE_COMPLETED:
            x = 3
        elif x == Order.ORDER_STATE_DISPATCHED:
            x = 4
        elif x == Order.ORDER_STATE_CANCELLED:
            x = 5
        else:
            continue

        corder.append(x)
        corder.append(order.delivery_addr)
        corders.append(corder)

    context = {
        "orders": corders,
    }

    return render(request, "users/order-list.html", context)
"""
