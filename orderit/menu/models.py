from django.db import models


# Create your models here.
from django.utils.timezone import now


class MenuItem(models.Model):
    # Items in menu will be from mo-fr, no food for people on saturdays and sundays
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    days = [(MONDAY, 'Monday'), (TUESDAY, 'Tuesday'), (WEDNESDAY, 'Wednesday'), (THURSDAY, 'Thursday'),
            (FRIDAY, 'Friday')]
    OPEN = 'open'
    CLOSED = 'closed'
    status = [(OPEN, 'open'), (CLOSED, 'closed')]
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    day = models.CharField(choices=days, max_length=14, default=MONDAY)
    created_date = models.DateTimeField(default=now, editable=False)
    # add status
    status = models.CharField(choices=status, max_length=7, default=OPEN)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    objects = None
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
