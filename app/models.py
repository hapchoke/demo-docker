from django.db.models.signals import post_save
from turtle import title
from unicodedata import category
from django.conf import settings
from django.db import models
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        # userごとの設定
    def __str__(self):
        return self.user.username

class Category(models.Model):
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.category



class Item(models.Model):
    title=models.CharField(max_length=30)
    price=models.IntegerField()
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app:detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("app:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("app:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)

    def __str__(self):
            return f'{self.quantity}of{self.item.title}'
        
    def get_total_item_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    order_date=models.DateTimeField(null=True,blank=True)
    ordered=models.BooleanField(default=False)
    address=models.ForeignKey('Address',blank=True,null=True,on_delete=models.SET_NULL)
    being_delivered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    ref_code=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
            return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    prefecture=models.CharField(max_length=10)
    street_address = models.CharField(max_length=50)
    apartment_address = models.CharField(max_length=50,blank=True,null=True)
    zip = models.CharField(max_length=8)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)