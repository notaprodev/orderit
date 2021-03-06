from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import DO_NOTHING
from django.db.models.signals import post_save


class UserRole(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Dep(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    user_role = models.ForeignKey(UserRole, on_delete=DO_NOTHING, blank=True, null=True)
    no_cel = models.CharField(max_length=20, blank=True)
    dep = models.ForeignKey(Dep, on_delete=DO_NOTHING, blank=True, null=True)
    money = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    money_unspent = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=20, blank=False)
    l_name = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=40, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    address = models.TextField()

    def __str__(self):
        return self.user.username



class Item(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30, blank=False)
    category = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.fname


"""
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivery_addr = models.CharField(max_length=50, blank=True)
    orderedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    r_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    ORDER_STATE_WAITING = "Waiting"
    ORDER_STATE_PLACED = "Placed"
    ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
    ORDER_STATE_COMPLETED = "Completed"
    ORDER_STATE_CANCELLED = "Cancelled"
    ORDER_STATE_DISPATCHED = "Dispatched"

    ORDER_STATE_CHOICES = (
        (ORDER_STATE_WAITING, ORDER_STATE_WAITING),
        (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
        (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
        (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
        (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
        (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
    )
    status = models.CharField(max_length=50, choices=ORDER_STATE_CHOICES, default=ORDER_STATE_WAITING)

    def __str__(self):
        return str(self.id) + ' ' + self.status"""


"""class orderItem(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ord_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)"""
