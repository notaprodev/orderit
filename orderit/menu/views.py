from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.db.models.fields import json
from django.shortcuts import render, redirect
from django.utils.timezone import datetime as td
# Create your views here.
from django.views import View

from .models import *


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
            return redirect('account_login')

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
            menu_items = MenuItem.objects.filter(day__icontains='Monday')  # datetime.today().strftime('%A'))

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
        return self.request.user.groups.filter(name='admins').exists()


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
        return self.request.user.groups.filter(name='admins').exists()
