from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.db.models.fields import json
from django.shortcuts import render, redirect
from django.utils.timezone import datetime as td
# Create your views here.
from django.views import View
from .forms import NewMenuItem
from .models import *
from users.models import CustomUser


class Order(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # get every item from each category for the current day
            appetizers = MenuItem.objects.filter(
                Q(category__name__contains='Appetizer') & Q(day__icontains='Monday') & Q
                (status__icontains='open'))  # datetime.today().strftime('%A')))
            entres = MenuItem.objects.filter(Q(category__name__contains='Entre') & Q(day__icontains='Monday') &
                                             Q(status__icontains='open'))
            desserts = MenuItem.objects.filter(Q(category__name__contains='Dessert') & Q(day__icontains='Monday') &
                                               Q(status__icontains='open'))
            drinks = MenuItem.objects.filter(Q(category__name__contains='Drink') & Q(day__icontains='Monday') &
                                             Q(status__icontains='open'))
            context = {
                'appetizers': appetizers,
                'entres': entres,
                'desserts': desserts,
                'drinks': drinks,
            }
            return render(request, 'menu/neworder.html', context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        global price, item_ids
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        if price < 5:
            order = OrderModel.objects.create(
                price=price,
                name=name,
                email=email,
                street=street,
            )
            order.items.add(*item_ids)
            return redirect('order-confirmation', pk=order.pk)
        else:
            appetizers = MenuItem.objects.filter(
                Q(category__name__contains='Appetizer') & Q(
                    day__icontains='Monday'))  # datetime.today().strftime('%A')))
            entres = MenuItem.objects.filter(Q(category__name__contains='Entre') & Q(day__icontains='Monday'))
            desserts = MenuItem.objects.filter(Q(category__name__contains='Dessert') & Q(day__icontains='Monday'))
            drinks = MenuItem.objects.filter(Q(category__name__contains='Drink') & Q(day__icontains='Monday'))
            err = 'your sum is higher then 5$'

            # pass into context
            context = {
                'appetizers': appetizers,
                'entres': entres,
                'desserts': desserts,
                'drinks': drinks,
                'err': err,
            }

            # render the template
            return render(request, 'menu/order.html', context)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'menu/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class Menu(View):
    # shows only meals for current day
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            menu_items = MenuItem.objects.filter(day__icontains='Tuesday')  # datetime.today().strftime('%A'))

            context = {
                'menu_items': menu_items
            }

            return render(request, 'menu/menu.html', context)
        else:
            return redirect('login')


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'menu/menu.html', context)


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = td.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'menu/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='admin').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'menu/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'menu/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='admin').exists()


def AddNewItem(request):
    if request.method == 'POST':
        form = NewMenuItem(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NewMenuItem()
    return render(request, 'menu/newitem.html', {'form': form})


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
        items_list = MenuItem.objects.filter(ord_id=order)

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
